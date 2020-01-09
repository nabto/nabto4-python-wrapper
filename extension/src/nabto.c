#include <Python.h>
#include <nabto_client_api.h>
#include <stdio.h>

static PyObject* NabtoError = NULL;

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

static struct PyModuleDef nabtoModule = {
    PyModuleDef_HEAD_INIT,
    "nabto",
    "Python interface for the Nabto client C API",
    -1,
    NabtoMethods
};

PyMODINIT_FUNC PyInit_nabto(void) {
    PyObject* module = PyModule_Create(&nabtoModule);

    NabtoError = PyErr_NewException("nabto.NabtoError", NULL, NULL);
    PyModule_AddObject(module, "NabtoError", NabtoError);

    return module;
}