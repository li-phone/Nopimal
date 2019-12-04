//
// Created by 97412 on 2019/12/1.
//

#ifndef __Operator_MODULE_CPP
#define __Operator_MODULE_CPP

#include <string>
#include <vector>
#include <time.h>
#include <sstream>
#include <map>
#include <algorithm>
#include <math.h>
#include <Python.h>


/*=============================================================== Operator C++ Module ===============================================================*/


constexpr auto INT32_NAN = 0x7FFFFFFF;
constexpr auto INT64_NAN = 0x7FFFFFFFFFFFFFFF;


using namespace std;


typedef struct FeatureAttribute {
	string name = "";
	string type = "";
	string transform = "";
	double unit = 1.0;
	string command = "";
	vector<string> operators;
	vector<double> group_dists;
	vector<string> splits;
	int start_index = 0;
	int end_index = 0;
}FeatureAttribute;


vector<string> str_split(string str, string split) {
	vector<string> v;
	int idx = 0;
	while (idx != string::npos)
	{
		int pos = str.find(split, idx);
		if (pos == string::npos)
		{
			break;
		}
		string _ = str.substr(idx, pos - idx);
		v.push_back(_);
		idx = pos + 1;
	}
	string _ = str.substr(idx, str.length() - idx);
	if (_ != "")
	{
		v.push_back(_);
	}
	return v;
}


double string2double(string str)
{
	double num;
	stringstream ss;
	ss << str;
	ss >> num;
	return num;
}


void vec_statistics(vector<double>v, double& sum, double& mean, double& max, double& min) {
	sum = 0;
	mean = 0;
	max = -1.0 * INFINITY;
	min = 1.0 * INFINITY;
	for (size_t i = 0; i < v.size(); i++)
	{
		sum += v[i];
		if (max < v[i])
		{
			max = v[i];
		}
		if (min > v[i])
		{
			min = v[i];
		}
	}
	if (v.size() > 0)
	{
		mean = sum / v.size();
	}
}


bool is_nan(string str) {
	return "" == str;
}


bool is_nan(int64_t n) {
	return INT64_NAN == n;
}


bool is_nan(int32_t n) {
	return INT32_NAN == n;
}


bool is_nan(float n) {
	return isnan(n);
}


bool is_nan(double n) {
	return isnan(n);
}


template<typename T>
map<T, int> vec_unique(vector<T> col) {
	map<T, int> m;
	for (size_t i = 0; i < col.size(); i++)
	{
		if (m.find(col[i]) != m.end())
		{
			m[col[i]] += 1;
		}
		else {
			m[col[i]] = 1;
		}
	}
	return m;
}


void map_key_value(vector<string>& keys, vector<int>& values, map<string, int>m) {
	keys.resize(m.size()); values.resize(m.size());
	int i = 0;
	for (map<string, int>::iterator it = m.begin(); it != m.end(); it++)
	{
		keys[i] = it->first;
		values[i] = it->second;
		i += 1;
	}
}


void map_key_value(vector<int64_t>& keys, vector<int>& values, map<int64_t, int>m) {
	keys.resize(m.size()); values.resize(m.size());
	int i = 0;
	for (map<int64_t, int>::iterator it = m.begin(); it != m.end(); it++)
	{
		keys[i] = it->first;
		values[i] = it->second;
		i += 1;
	}
}


void map_key_value(vector<float>& keys, vector<int>& values, map<float, int>m) {
	keys.resize(m.size()); values.resize(m.size());
	int i = 0;
	for (map<float, int>::iterator it = m.begin(); it != m.end(); it++)
	{
		keys[i] = it->first;
		values[i] = it->second;
		i += 1;
	}
}


void map_key_value(vector<double>& keys, vector<int>& values, map<double, int>m) {
	keys.resize(m.size()); values.resize(m.size());
	int i = 0;
	for (map<double, int>::iterator it = m.begin(); it != m.end(); it++)
	{
		keys[i] = it->first;
		values[i] = it->second;
		i += 1;
	}
}


template<typename T>
void vec_where(vector<T>& vals, vector<int>& idxs, vector<T>col, T target) {
	vals.resize(0); idxs.resize(0);
	for (size_t i = 0; i < col.size(); i++)
	{
		if (col[i] == target)
		{
			vals.push_back(col[i]);
			idxs.push_back(i);
		}
	}
}


template<typename T>
vector<T> vec_keep(vector<T> col, vector<int> idxs) {
	vector<T> keep_col(idxs.size());
	for (size_t i = 0; i < idxs.size(); i++)
	{
		keep_col[i] = col[idxs[i]];
	}
	return keep_col;
}


template<typename T>
int template_index(vector<T> vecs, T s) {
	for (size_t i = 0; i < vecs.size(); i++)
	{
		if (s == vecs[i])
		{
			return i;
		}
	}
	return -1;
}


int get_tm_type(struct tm* t, string type) {
	if ("sec" == type) {
		return t->tm_sec;
	}
	else if ("min" == type) {
		return t->tm_min;
	}
	else if ("hour" == type)
	{
		return t->tm_hour;
	}
	else if ("mday" == type)
	{
		return t->tm_mday;
	}
	else if ("mon" == type)
	{
		return t->tm_mon;
	}
	else if ("year" == type)
	{
		return t->tm_year + 1900;
	}
	else if ("wday" == type)
	{
		return t->tm_wday;
	}
	else if ("yday" == type)
	{
		return t->tm_yday;
	}
	else if ("isdst" == type)
	{
		return t->tm_isdst;
	}
	else {
		return -1;
	}
}


template<typename T>
void _operator_col(
	vector < vector<T>>& outFeatures, vector < vector<bool>>& outFeaIndexs, vector<FeatureAttribute>& outFeaAttribs,
	vector<T>& col, vector<bool>& index, FeatureAttribute feaAttrib)
{
	outFeatures.resize(0); outFeaIndexs.resize(0); outFeaAttribs.resize(0);
	if ("timestamp" == feaAttrib.command)
	{
		vector<struct tm*> ttimes(col.size());
		for (size_t i = 0; i < col.size(); i++)
		{
			if (col[i] < 0 && is_nan(col[i]))
			{
				index[i] = true;
			}
			if (false == index[i])
			{
				time_t tt = col[i];
				struct tm* ttime;
				ttime = localtime(&tt);
				ttimes[i] = ttime;
			}
		}
		for (vector<string>::iterator op = feaAttrib.operators.begin(); op != feaAttrib.operators.end(); op++)
		{
			FeatureAttribute outFeaAttrib;
			outFeaAttrib.name = feaAttrib.name + "_" + *op;
			vector<double> outFeature(ttimes.size());
			for (size_t i = 0; i < ttimes.size(); i++)
			{
				if (false == index[i])
				{
					outFeature[i] = get_tm_type(ttimes[i], *op);
				}
			}
			outFeaAttribs.push_back(outFeaAttrib);
			outFeatures.push_back(outFeature);
			outFeaIndexs.push_back(index);
		}
	}
	else if ("group" == feaAttrib.command)
	{
		for (size_t i = 0; i < col.size(); i++)
		{
			if (false == index[i])
			{
				for (vector<double>::iterator it = feaAttrib.group_dists.begin(); it != feaAttrib.group_dists.end(); it++)
				{
					double grp_dist = *it;
					if (grp_dist > 0)
					{
						col[i] = int(col[i] * 1.0 / grp_dist);
					}
				}
			}
		}
		outFeaAttribs.push_back(feaAttrib);
		outFeatures.push_back(col);
		outFeaIndexs.push_back(index);
	}
}


void _operator_col(
	vector < vector<double>>& outFeatures, vector < vector<bool>>& outFeaIndexs, vector<FeatureAttribute>& outFeaAttribs,
	vector<string>& col, vector<bool>& index, FeatureAttribute feaAttrib)
{
	outFeatures.resize(0); outFeaIndexs.resize(0); outFeaAttribs.resize(0);
	if ("split" == feaAttrib.command)
	{
		vector<vector<string>> split_groups(col.size());
		for (size_t i = 0; i < col.size(); i++)
		{
			vector<string> split_group;
			if (false == index[i])
			{
				if (feaAttrib.start_index != feaAttrib.end_index)
				{
					if (feaAttrib.end_index < 0)
					{
						if (feaAttrib.start_index <= col[i].length())
						{
							col[i] = col[i].substr(feaAttrib.start_index, col[i].length() + feaAttrib.end_index - feaAttrib.start_index);

						}

					}
					else {
						col[i] = col[i].substr(feaAttrib.start_index, feaAttrib.end_index);

					}

				}
				split_group = str_split(col[i], feaAttrib.splits[0]);
				for (size_t j = 0; j < split_group.size(); j++)
				{
					for (size_t k = 1; k < feaAttrib.splits.size(); k++)
					{
						vector<string> s = str_split(split_group[j], feaAttrib.splits[k]);
						if (s.size() >= 2)
						{
							split_group[j] = s[1];
							if ("" == split_group[j])
							{
								split_group[j] = "0";
							}
						}
						else {
							split_group[j] = "0";
						}

					}
				}
			}
			split_groups[i] = split_group;
		}
		vector<vector<double>> split_values(col.size());
		vector<double> split_sums(col.size()), split_means(col.size()), split_maxs(col.size()), split_mins(col.size());
		if (feaAttrib.operators.size() >= 2)
		{

			for (size_t i = 0; i < split_groups.size(); i++)
			{
				vector<double> split_value;
				if (false == index[i])
				{
					for (size_t j = 0; j < split_groups[i].size(); j++)
					{
						double f = string2double(split_groups[i][j]);
						split_value.push_back(f);
					}
					split_values[i] = split_value;
					double sum, mean, max, min;
					vec_statistics(split_value, sum, mean, max, min);
					split_sums[i] = sum;
					split_means[i] = mean;
					split_maxs[i] = max;
					split_mins[i] = min;
				}
			}
		}
		else {
			for (size_t i = 0; i < split_groups.size(); i++)
			{
				vector<double> split_value;
				if (false == index[i])
				{
					for (size_t j = 0; j < split_groups[i].size(); j++)
					{
						double f = 1.0;
						split_value.push_back(f);
					}
					split_values[i] = split_value;
				}
			}
		}

		for (size_t i = 0; i < feaAttrib.operators.size(); i++)
		{
			if ("len" == feaAttrib.operators[i])
			{
				FeatureAttribute outFeaAttrib;
				outFeaAttrib.name = feaAttrib.name + "_len";
				vector<double> outFeature(col.size());
				for (size_t j = 0; j < outFeature.size(); j++)
				{
					if (false == index[j])
					{
						outFeature[j] = split_values[j].size();
						double grp_dist = feaAttrib.group_dists[i];
						if (grp_dist > 0)
						{
							outFeature[j] = int(outFeature[j] * 1.0 / grp_dist);
						}
					}
				}
				outFeaAttribs.push_back(outFeaAttrib);
				outFeatures.push_back(outFeature);
				outFeaIndexs.push_back(index);
			}
			else if ("sum" == feaAttrib.operators[i])
			{
				FeatureAttribute outFeaAttrib;
				outFeaAttrib.name = feaAttrib.name + "_sum";
				for (size_t j = 0; j < split_sums.size(); j++)
				{
					if (false == index[j])
					{
						double grp_dist = feaAttrib.group_dists[i];
						if (grp_dist > 0)
						{
							split_sums[j] = int(split_sums[j] * 1.0 / grp_dist);
						}
					}
				}
				outFeaAttribs.push_back(outFeaAttrib);
				outFeatures.push_back(split_sums);
				outFeaIndexs.push_back(index);
			}
			else if ("mean" == feaAttrib.operators[i])
			{
				FeatureAttribute outFeaAttrib;
				outFeaAttrib.name = feaAttrib.name + "_mean";
				for (size_t j = 0; j < split_means.size(); j++)
				{
					if (false == index[j])
					{
						double grp_dist = feaAttrib.group_dists[i];
						if (grp_dist > 0)
						{
							split_means[j] = int(split_means[j] * 1.0 / grp_dist);
						}
					}
				}
				outFeaAttribs.push_back(outFeaAttrib);
				outFeatures.push_back(split_means);
				outFeaIndexs.push_back(index);
			}
			else if ("max" == feaAttrib.operators[i])
			{
				FeatureAttribute outFeaAttrib;
				outFeaAttrib.name = feaAttrib.name + "_max";
				for (size_t j = 0; j < split_maxs.size(); j++)
				{
					if (false == index[j])
					{
						double grp_dist = feaAttrib.group_dists[i];
						if (grp_dist > 0)
						{
							split_maxs[j] = int(split_maxs[j] * 1.0 / grp_dist);
						}
					}
				}
				outFeaAttribs.push_back(outFeaAttrib);
				outFeatures.push_back(split_maxs);
				outFeaIndexs.push_back(index);
			}
			else if ("min" == feaAttrib.operators[i])
			{
				FeatureAttribute outFeaAttrib;
				outFeaAttrib.name = feaAttrib.name + "_min";
				for (size_t j = 0; j < split_mins.size(); j++)
				{
					if (false == index[j])
					{
						double grp_dist = feaAttrib.group_dists[i];
						if (grp_dist > 0)
						{
							split_mins[j] = int(split_mins[j] * 1.0 / grp_dist);
						}
					}
				}
				outFeaAttribs.push_back(outFeaAttrib);
				outFeatures.push_back(split_mins);
				outFeaIndexs.push_back(index);
			}
		}
	}
}


template<typename T>
vector < vector<double>> _col2feature(
	vector<FeatureAttribute>& outFeaAttribs,
	vector<T>& col,
	vector<bool>& index,
	FeatureAttribute feaAttrib,
	vector<T> labels,
	vector<string> featureNames,
	vector<vector<double>> featureValues)
{
	outFeaAttribs.resize(featureNames.size());
	vector < vector<double>> outFeatures(featureNames.size());
	for (size_t i = 0; i < featureNames.size(); i++)
	{
		vector<double> outFeature(col.size(), 0);
		outFeatures[i] = outFeature;
		FeatureAttribute outFeaAttrib;
		outFeaAttrib.name = feaAttrib.name + "_" + featureNames[i];
		outFeaAttribs[i] = outFeaAttrib;
	}
	for (size_t i = 0; i < col.size(); i++)
	{
		int idx = -1;
		T label = col[i];
		idx = template_index(labels, label);
		if (-1 != idx)
		{
			for (size_t j = 0; j < featureNames.size(); j++)
			{
				outFeatures[j][i] = featureValues[j][idx];
			}
		}
		else {
			index[i] = true;
			string warning_str = "Warning!!! Labels have no such " + label + "!\n";
			printf(warning_str.c_str());
		}
	}
	return outFeatures;
}


template<typename T>
void _format_col(vector<T>& col, vector<bool>& index, FeatureAttribute feaAttrib) {
	for (size_t i = 0; i < col.size(); i++)
	{
		if (false == index[i])
		{
			double grp_dist = feaAttrib.unit;
			col[i] = col[i] * 1.0 / grp_dist;
		}
	}
}


void _format_col(vector<string>& col, vector<bool>& index, FeatureAttribute feaAttrib) {
	for (size_t i = 0; i < col.size(); i++)
	{
		if (false == index[i])
		{
			if ("lower" == feaAttrib.transform)
			{
				transform(col[i].begin(), col[i].end(), col[i].begin(), ::tolower);

			}
			else
				if ("upper" == feaAttrib.transform)
				{
					transform(col[i].begin(), col[i].end(), col[i].begin(), ::toupper);

				}
		}
	}
}


template<typename T>
void _count_col(vector<vector<int>>& col_cnts, vector<int64_t>targets, vector<T> col, int64_t& click_nums, int64_t target = 1) {
	map<int64_t, int> target_map = vec_unique(targets);
	vector<int64_t> target_keys;
	vector<int> target_values;
	map_key_value(target_keys, target_values, target_map);
	sort(target_keys.begin(), target_keys.end());

	map<T, int> col_map = vec_unique(col);
	vector<T> col_keys;
	vector<int> col_values;
	map_key_value(col_keys, col_values, col_map);
	col_cnts.resize(col_keys.size());
	for (size_t i = 0; i < col_keys.size(); i++)
	{
		vector<int64_t>keep_vals;
		vector<int>keep_idxs;
		vec_where(keep_vals, keep_idxs, col, col_keys[i]);
		vector<int64_t> keep_target = vec_keep(targets, keep_idxs);
		vector<int> cnt(target_keys.size(), 0);
		for (size_t j = 0; j < target_keys.size(); j++)
		{
			map<int64_t, int> keep_target_map = vec_unique(keep_target);
			if (keep_target_map.find(target_keys[j]) != keep_target_map.end())
			{
				cnt[j] = keep_target_map[target_keys[j]];
			}
			else {
				cnt[j] = 0;
			}
		}
		col_cnts[i] = cnt;
	}
	click_nums = target_map[target];
}


/*=============================================================== Operator Python Module API ===============================================================*/


int max(vector<int64_t> lst) {
	int max_num = INT_MIN;
	for (int i = 0; i < lst.size(); i++) {
		if (lst[i] > max_num) {
			max_num = lst[i];
		}
	}
	return max_num;
}


vector<int64_t> parsePyObject(PyObject** obj)
{
	vector<int64_t> lst;
	// 获取可迭代对象
	PyObject* iter = PyObject_GetIter(*obj);
	if (!iter) {
		PyErr_SetString(PyExc_TypeError, "The object is not iterable!");
		return lst;
	}

	while (true) {
		// 逐个获取列表中的各个元素
		PyObject* next = PyIter_Next(iter);
		char* c_pstr = PyBytes_AsString(next);   // 转成C的字符指针
		PyErr_SetString(PyExc_TypeError, c_pstr);
		if (!next) {
			break;
		}
		// 检查是否为long或者long的子类（包括int）
		if (!PyLong_Check(next)) {
			PyErr_SetString(PyExc_TypeError, "Int or Long list is expected!");
			return lst;
		}
		// 由Python的Long转化为C/C++的long
		int64_t num = PyLong_AsLongLong(next);
		lst.push_back(num);
	}
	return lst;
}

// 模块中每个可供Python调用的函数都需要一个对应的包裹函数
static PyObject* Operator_max(PyObject* self, PyObject* args) {
	PyObject* obj;
	// O代表对象
	if (!PyArg_ParseTuple(args, "O", &obj)) {
		return NULL;
	}

	vector<int64_t> lst = parsePyObject(&obj);
	return (PyObject*)Py_BuildValue("L", max(lst));
}

// 添加PyMethodDef ModuleMethods[]数组
static PyMethodDef OperatorMethods[] = {
	// add：可用于Python调用的函数名，Exten_add：C++中对应的函数名
	{"max",Operator_max,METH_VARARGS},
	{NULL,NULL},
};

// 初始化函数
static struct PyModuleDef OperatorModule = {
	PyModuleDef_HEAD_INIT,
	"Operator",//模块名称
	NULL,
	-1,
	OperatorMethods
};


void PyInit_Operator() {
	PyModule_Create(&OperatorModule);
}


#ifdef TEST_FLAG
bool test_operator_col_double() {
	vector < vector<double>> outFeatures;
	vector < vector<bool>> outFeaIndexs;
	vector<FeatureAttribute> outFeaAttribs;
	vector<double> col(2);
	vector<bool> index(2);
	FeatureAttribute feaAttrib;
	col[0] = 3;
	col[1] = 666;
	index[0] = true;
	index[1] = false;
	feaAttrib.name = "testName";
	feaAttrib.command = "None";
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
	feaAttrib.command = ""; outFeatures.clear(); outFeaIndexs; outFeaAttribs.clear();

	col[0] = 1234567890;
	col[1] = 2234567890;
	index[0] = true;
	index[1] = false;
	feaAttrib.name = "testName";
	feaAttrib.command = "timestamp";
	feaAttrib.operators.push_back("sec");
	feaAttrib.operators.push_back("min");
	feaAttrib.operators.push_back("hour");
	feaAttrib.operators.push_back("mday");
	feaAttrib.operators.push_back("mon");
	feaAttrib.operators.push_back("year");
	feaAttrib.operators.push_back("wday");
	feaAttrib.operators.push_back("yday");
	feaAttrib.operators.push_back("isdst");
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
	feaAttrib.command = ""; outFeatures.clear(); outFeaIndexs; outFeaAttribs.clear();

	col[0] = 3;
	col[1] = 666;
	index[0] = true;
	index[1] = false;
	feaAttrib.name = "testName";
	feaAttrib.command = "group";
	feaAttrib.group_dists.push_back(2);
	feaAttrib.group_dists.push_back(5);
	feaAttrib.group_dists.push_back(0.2);
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
	col.clear(); feaAttrib.command = ""; outFeatures.clear(); outFeaIndexs; outFeaAttribs.clear();
	printf("test_operator_col_double () test ok!\n");
	return true;
}


bool test_operator_col_string() {
	vector < vector<double>> outFeatures;
	vector < vector<bool>> outFeaIndexs;
	vector<FeatureAttribute> outFeaAttribs;
	vector<string> col(2);
	vector<bool> index(2);
	FeatureAttribute feaAttrib;

	col[0] = "a:3.4|b:6.5";
	col[1] = "abb:56.62234567890|bbb:";
	index[0] = false;
	index[1] = false;
	feaAttrib.name = "testName";
	feaAttrib.command = "split";
	feaAttrib.operators.push_back("len");
	feaAttrib.operators.push_back("sum");
	feaAttrib.operators.push_back("mean");
	feaAttrib.operators.push_back("max");
	feaAttrib.operators.push_back("min");
	feaAttrib.splits.push_back("|");
	feaAttrib.splits.push_back(":");
	feaAttrib.group_dists.push_back(2);
	feaAttrib.group_dists.push_back(5);
	feaAttrib.group_dists.push_back(0.2);
	feaAttrib.group_dists.push_back(5);
	feaAttrib.group_dists.push_back(0.2);
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
	outFeatures.clear(), outFeaIndexs.clear(), feaAttrib.operators.clear(), feaAttrib.splits.clear(), feaAttrib.group_dists.clear();

	col[0] = "[app_1 ]";
	col[1] = "";
	index[0] = false;
	index[1] = false;
	feaAttrib.name = "testName";
	feaAttrib.command = "split";
	feaAttrib.operators.push_back("len");
	feaAttrib.splits.push_back(" ");
	feaAttrib.group_dists.push_back(0.2);
	feaAttrib.start_index = 1;
	feaAttrib.end_index = -2;
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
	printf("test_operator_col_string () test ok!\n");
	return true;
}


bool test_col2feature() {
	vector<FeatureAttribute> outFeaAttribs;
	vector<string> col(3);
	vector<bool> index(3);
	FeatureAttribute feaAttrib;
	vector<string> labels(2);
	vector<string> featureNames(3);
	vector<vector<double>> featureValues(3);
	col[0] = "1"; col[1] = "2"; col[2] = "3";
	index[0] = false;
	index[1] = false;
	index[2] = false;
	feaAttrib.name = "testName";
	labels[0] = "1", labels[1] = "2";
	featureNames[0] = "A", featureNames[1] = "B", featureNames[2] = "C";
	featureValues[0] = vector<double>(2);
	featureValues[1] = vector<double>(2);
	featureValues[2] = vector<double>(2);
	featureValues[0][0] = 0, featureValues[0][1] = 1, featureValues[1][0] = 2;
	featureValues[1][1] = 3, featureValues[2][0] = 4, featureValues[2][1] = 6;
	vector < vector<double>> result = _col2feature(outFeaAttribs, col, index, feaAttrib, labels, featureNames, featureValues);
	printf("test_col2feature () test ok!\n");
	return true;
}


bool test_count_col() {
	vector<vector<int>>col_cnts;
	vector<int64_t>targets(3);
	vector<int64_t> col(3);
	int64_t click_nums;
	targets[0] = 1; targets[1] = 0; targets[2] = 1;
	col[0] = 1; col[1] = 2; col[2] = 1;
	_count_col(col_cnts, targets, col, click_nums);
	printf("test_count_col () test ok!\n");
	return true;
}


int main(int argc, char* argv[])
{
	test_operator_col_double();
	test_operator_col_string();
	test_col2feature();
	test_count_col();
	return 0;
}
#endif // TEST_FLAG

#endif // !__Operator_MODULE_CPP
