#include <Python.h>
#include <structmember.h>
#include <stdio.h>
#include "nabto_client_api.h"

static PyObject* NabtoError = NULL;

typedef struct {
    PyObject_HEAD
    nabto_handle_t session;
} SessionObject;

// Session API

static PyObject* py_nabtoStartup(PyObject* self, PyObject *args) {
    printf("nabtoStartup\n");
    char *homeDir = NULL;
    if (!PyArg_ParseTuple(args, "s", &homeDir)) {
        return NULL;
    }

    nabto_status_t st = nabtoStartup(homeDir);
    if (st != NABTO_OK) {
        PyErr_SetString(NabtoError, nabtoStatusStr(st));
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject* py_nabtoShutdown(PyObject* self, PyObject *args) {
    printf("nabtoShutdown\n");
    nabto_status_t st = nabtoShutdown();
    if (st != NABTO_OK) {
        PyErr_SetString(NabtoError, nabtoStatusStr(st));
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject* py_nabtoVersionString(PyObject* self, PyObject *args) {
    char* version;
    nabto_status_t st = nabtoVersionString(&version);
    if (st != NABTO_OK) {
        PyErr_SetString(NabtoError, nabtoStatusStr(st));
        return NULL;
    }

    PyObject* result = PyUnicode_FromString(version);
    nabtoFree(version);
    return result;
}

static void Session_dealloc(SessionObject *self) {
    if (self->session != NULL) {
        nabto_status_t st = nabtoCloseSession(self->session);
        if (st != NABTO_OK) {
            PyErr_SetString(NabtoError, nabtoStatusStr(st));
            return;
        }
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* Session_open(SessionObject* self, PyObject *args) {
    printf("Session.open\n");
    char* id = NULL;
    char* password = NULL;
    if (!PyArg_ParseTuple(args, "ss", &id, &password)) {
        return NULL;
    }
    nabto_status_t st = nabtoOpenSession(&self->session, id, password);
    if (st != NABTO_OK) {
        PyErr_SetString(NabtoError, nabtoStatusStr(st));
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject* Session_close(SessionObject* self, PyObject *Py_UNUSED(ignored)) {
    printf("Session.close\n");
    nabto_handle_t session = self->session;
    self->session = NULL;
    nabto_status_t st = nabtoCloseSession(session);
    if (st != NABTO_OK) {
        PyErr_SetString(NabtoError, nabtoStatusStr(st));
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject* Session_rpcSetDefaultInterface(SessionObject* self, PyObject *args) {
    printf("Session.rpcSetDefaultInterface\n");
    char* interfaceDefinition = NULL;
    char* err = NULL;
    if (!PyArg_ParseTuple(args, "s", &interfaceDefinition)) {
        return NULL;
    }
    nabto_status_t st = nabtoRpcSetDefaultInterface(self->session, interfaceDefinition, &err);
    if (st != NABTO_OK) {
        if (st == NABTO_FAILED_WITH_JSON_MESSAGE) {
            PyErr_SetString(NabtoError, err);
            nabtoFree(err);
            return NULL;
        }
        PyErr_SetString(NabtoError, nabtoStatusStr(st));
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject* Session_rpcInvoke(SessionObject* self, PyObject *args) {
    printf("Session.rpcInvoke\n");
    char* url = NULL;
    char* response = NULL;
    if (!PyArg_ParseTuple(args, "s", &url)) {
        return NULL;
    }
    nabto_status_t st = nabtoRpcInvoke(self->session, url, &response);
    PyObject* result = PyUnicode_FromString(response);
    nabtoFree(response);
    if (st != NABTO_OK) {
        PyErr_SetString(NabtoError, nabtoStatusStr(st));
        return NULL;
    }
    return result;
}

static PyMethodDef NabtoMethods[] = {
    {
        "nabtoStartup", py_nabtoStartup, METH_VARARGS, "Initializes the Nabto client API"
    },
    {
        "nabtoShutdown", py_nabtoShutdown, METH_NOARGS, "Terminates the Nabto client API"
    },
    {
        "nabtoVersionString", py_nabtoVersionString, METH_NOARGS, "Get the underlying C libs Nabto software version (major.minor.patch[-prerelease tag]+build)"
    },
    {
        NULL, NULL, 0, NULL
    }
};

static PyMethodDef SessionMethods[] = {
    {
        "open", (PyCFunction) Session_open, METH_VARARGS, 
        "Starts a new Nabto session as context for RPC, stream or tunnel invocation using the specified profile."
    },
    {
        "close", (PyCFunction) Session_close, METH_VARARGS,
        "Closes the specified Nabto session and frees internal ressources."
    },
    {
        "rpcSetDefaultInterface", (PyCFunction) Session_rpcSetDefaultInterface, METH_VARARGS,
        "Sets the default RPC interface to use when later invoking Session.rpcInvoke()."
    },
    {
        "rpcInvoke", (PyCFunction) Session_rpcInvoke, METH_VARARGS,
        "Retrieves data synchronously from specified nabto:// URL on specified session"
    },
    {
        NULL, NULL, 0, NULL
    }
};

static PyTypeObject SessionType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "nabto.Session",
    .tp_doc = "Session object",
    .tp_basicsize = sizeof(SessionObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor) Session_dealloc,
    .tp_methods = SessionMethods,
};

static struct PyModuleDef nabtoModule = {
    PyModuleDef_HEAD_INIT,
    "nabto",
    "Python interface for the Nabto client C API",
    -1,
    NabtoMethods
};

PyMODINIT_FUNC PyInit_nabto(void) {
    if (PyType_Ready(&SessionType) < 0) {
        return NULL;
    }

    PyObject* module = PyModule_Create(&nabtoModule);

    NabtoError = PyErr_NewException("nabto.NabtoError", NULL, NULL);
    PyModule_AddObject(module, "NabtoError", NabtoError);

    Py_INCREF(&SessionType);
    if (PyModule_AddObject(module, "Session", (PyObject*)&SessionType) < 0) {
        Py_DECREF(&SessionType);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}