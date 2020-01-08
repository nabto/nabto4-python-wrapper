#include <Python.h>
#include <stdio.h>

static PyObject* nabtoStartup(PyObject* self, PyObject *args) {
    char *homeDir = NULL;

    if (!PyArg_ParseTuple(args, "s", &homeDir)) {
        return NULL;
    }

    printf("Nabto home directory is: %s\n", homeDir);

    Py_RETURN_NONE;
}

static PyMethodDef NabtoMethods[] = {
    {
        "nabtoStartup", nabtoStartup, METH_VARARGS, "Initializes the Nabto client API"
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
    return PyModule_Create(&nabtoModule);
}