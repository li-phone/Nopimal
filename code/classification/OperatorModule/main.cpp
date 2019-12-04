#include <Python.h>
#include <string>
#include <iostream>
#include <vector>


using namespace std;

vector<int64_t> PyList_AsVecInt(PyObject** pyList)
{
    Py_ssize_t pyList_size = PyList_Size(*pyList);
    vector<int64_t> vec_int(pyList_size);
    for (Py_ssize_t i = 0; i < pyList_size; ++i)
    {
        PyObject* obj = PyList_GetItem(*pyList, i);
        vec_int[i] = PyLong_Check(obj) ? PyLong_AsLongLong(obj) : INT64_MAX;
    }
    return vec_int;
}

vector<double> PyList_AsVecDouble(PyObject** pyList)
{
    Py_ssize_t pyList_size = PyList_Size(*pyList);
    vector<double> vec_double(pyList_size);
    for (Py_ssize_t i = 0; i < pyList_size; ++i)
    {
        PyObject* obj = PyList_GetItem(*pyList, i);
        vec_double[i] = PyFloat_Check(obj) ? PyFloat_AsDouble(obj) : NAN;
    }
    return vec_double;
}

vector<string> PyList_AsVecUTF8Str(PyObject** pyList)
{
    Py_ssize_t pyList_size = PyList_Size(*pyList);
    vector<string> vec_str(pyList_size);
    for (Py_ssize_t i = 0; i < pyList_size; ++i)
    {
        PyObject* obj = PyList_GetItem(*pyList, i);
        vec_str[i] = PyUnicode_Check(obj) ? PyUnicode_AsUTF8(obj) : "";
    }
    return vec_str;
}

//int Proc_PyDict(PyObject* pyValue)
//{
//	PyObject* key_dict = PyDict_Keys(pyValue); //return PyListObject
//	Py_ssize_t len = PyDict_Size(pyValue);
//
//	//forѭ��һ���ֵ��е�key��valueֵ
//	for (Py_ssize_t i = 0; i < len; ++i)
//	{
//		PyObject* key = PyList_GetItem(key_dict, i); // ����Ԫ��
//		size_t lent = PyTuple_Size(key);
//		//һ��key���ж��ֵ��ʱ�򣬰�key����Tuple��forѭ��һ��key�еĶ��ֵ
//		for (size_t k = 0; k < lent; ++k)
//		{
//			PyObject* item = PyTuple_GetItem(key, k);
//			// if(PyInt_Check(item))�ж�key��ֵ�ǲ���int���͵�,����ֵΪ��ture��
//			if (PyInt_Check(item))
//			{
//				//PyInt_AsLong��PyObject�е�Int����ת����c++�е�long����
//				long key = PyInt_AsLong(item);
//				cout << key << endl;
//			}
//			// if(PyString_Check(item))�ж�key��ֵ�ǲ���string���͵�,����ֵΪ��ture��
//			if (PyString_Check(item))
//			{
//				//PyString_AsString��PyObject�е�String����ת����c++�е�String����
//				string key = PyString_AsString(item);
//				cout << key << endl;
//			}
//		}
//		//��ӡvalue��ֵ
//		PyObject* value = PyDict_GetItem(pyValue, key); //��ѯvalue
//		string cval = PyString_AsString(value); //ת�����
//		cout << cval << endl;
//	}
//	return 0;
//}

int main()
{
    Py_SetPythonHome(L"D:/Install/Anaconda3");
    Py_Initialize(); //��ʼPython������
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");

    PyObject* pModule;
    PyObject* py_func;
    pModule = PyImport_ImportModule("operator_legacy");
    pModule = PyImport_ImportModule("cal");
    py_func = PyObject_GetAttrString(pModule, "mix");
    PyObject* py_ret_value = PyObject_CallFunction(py_func, NULL);

    vector<double> vec_double = PyList_AsVecDouble(&py_ret_value);
    vector<string> vec_str = PyList_AsVecUTF8Str(&py_ret_value);
    vector<int64_t> vec_int = PyList_AsVecInt(&py_ret_value);

    Py_ssize_t len = PyTuple_Size(py_ret_value);
    //forѭ��py�ļ����м����ֵ�
    for (Py_ssize_t i = 0; i < len; ++i) {
        PyObject* pyDict = PyTuple_GetItem(py_ret_value, i);
        //Proc_PyDict(pyDict);
    }

    Py_Finalize();
    system("pause");
    return 0;
}

