#include "python.h" 
#include <algorithm>
#include <vector>

static PyObject* spam_strlen(PyObject* self, PyObject* args)
{
	const char* str = NULL;
	int len;

	if (!PyArg_ParseTuple(args, "s", &str)) // �Ű����� ���� �м��ϰ� ���������� �Ҵ� ��ŵ�ϴ�.
		return NULL;

	len = strlen(str);

	return Py_BuildValue("i", len);
}

static PyObject* spam_max(PyObject* self, PyObject* args)
{
    PyObject* dict = NULL;
    if (!PyArg_ParseTuple(args, "O!", &PyDict_Type, &dict))
        return NULL;

    PyObject* values = PyDict_Values(dict);
    Py_ssize_t size = PyList_Size(values);
    std::vector<int> int_values;

    for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject* item = PyList_GetItem(values, i);
        if (PyLong_Check(item)) {
            int_values.push_back((int)PyLong_AsLong(item));
        }
    }

    Py_DECREF(values);

    if (int_values.empty()) {
        Py_RETURN_NONE;
    }

    int max_value = *std::max_element(int_values.begin(), int_values.end());

    return Py_BuildValue("i", max_value);
}


static PyMethodDef SpamMethods[] = {
    { "strlen", spam_strlen, METH_VARARGS, "count a string length." },
    { "spam_max", spam_max, METH_VARARGS, "find the maximum value in a dictionary." },
    { NULL, NULL, 0, NULL }// �迭�� ���� ��Ÿ���ϴ�.
};

static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",            // ��� �̸�
	"It is test module.", // ��� ������ ���� �κ�, ����� __doc__�� ����˴ϴ�.
	-1,SpamMethods
};


PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}
