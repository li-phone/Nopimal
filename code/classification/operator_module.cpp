//
// Created by 97412 on 2019/12/1.
//
//# MIT License
//#
//# Copyright(c)[2019][liphone / lifeng][email:974122407@qq.com]
//#
//# Permission is hereby granted, free of charge, to any person obtaining a copy
//# of this softwareand associated documentation files(the "Software"), to deal
//# in the Software without restriction, including without limitation the rights
//# to use, copy, modify, merge, publish, distribute, sublicense, and /or sell
//# copies of the Software, and to permit persons to whom the Software is
//# furnished to do so, subject to the following conditions :
//#
//# The above copyright noticeand this permission notice shall be included in all
//# copies or substantial portions of the Software.
//#
//# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
//# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//# SOFTWARE.

#ifndef __UTILS_MODULE_CPP
#define __UTILS_MODULE_CPP

#include <string>
#include <vector>
#include <time.h>
#include <sstream>
#include <map>
#include <algorithm>
#include <math.h>
#include <Python.h>
#include <iostream>


using namespace std;


constexpr auto INT32_NAN = 0x7FFFFFFF;
constexpr auto INT64_NAN = 0x7FFFFFFFFFFFFFFF;


#ifdef REGION
#undef REGION
#endif // REGION


/*============================================================= Operator C++ Module =============================================================*/
#ifndef REGION

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


struct tm tm_pt_2_tm_struct(struct tm* tp) {
	struct tm t;
	t.tm_sec = tp->tm_sec;
	t.tm_min = tp->tm_min;
	t.tm_hour = tp->tm_hour;
	t.tm_mday = tp->tm_mday;
	t.tm_mon = tp->tm_mon;
	t.tm_wday = tp->tm_wday;
	t.tm_yday = tp->tm_yday;
	t.tm_year = tp->tm_year;
	t.tm_isdst = tp->tm_isdst;
	return t;
}


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
map<T, int> vec_unique(vector<T> col, vector<T>& keys) {
	keys.resize(0);
	map<T, int> m;
	for (size_t i = 0; i < col.size(); i++)
	{
		if (m.find(col[i]) != m.end())
		{
			m[col[i]] += 1;
		}
		else {
			m[col[i]] = 1;
			keys.push_back(col[i]);
		}
	}
	return m;
}


template<typename T>
vector<int64_t> map_key_value(map<T, int>m, vector<T> keys) {
	vector<int64_t> values(keys.size());
	for (size_t i = 0; i < keys.size(); i++)
	{
		values[i] = m[keys[i]];
	}
	return values;
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


int get_tm_type(struct tm t, string type) {
	if ("sec" == type) {
		return t.tm_sec;
	}
	else if ("min" == type) {
		return t.tm_min;
	}
	else if ("hour" == type)
	{
		return t.tm_hour;
	}
	else if ("mday" == type)
	{
		return t.tm_mday;
	}
	else if ("mon" == type)
	{
		return t.tm_mon;
	}
	else if ("year" == type)
	{
		return t.tm_year + 1900;
	}
	else if ("wday" == type)
	{
		return t.tm_wday;
	}
	else if ("yday" == type)
	{
		return t.tm_yday;
	}
	else if ("isdst" == type)
	{
		return t.tm_isdst;
	}
	else {
		return -1;
	}
}


template<typename T>
void _operator_col(
	vector < vector<int64_t>>& outFeatures, vector < vector<bool>>& outFeaIndexs, vector<FeatureAttribute>& outFeaAttribs,
	vector<T>& col, vector<bool>& index, FeatureAttribute feaAttrib)
{
	outFeatures.resize(0); outFeaIndexs.resize(0); outFeaAttribs.resize(0);
	if ("timestamp" == feaAttrib.command)
	{
		vector<struct tm> ttimes(col.size());
		for (size_t i = 0; i < col.size(); i++)
		{
			if (col[i] < 0 || is_nan(col[i]))
			{
				index[i] = true;
			}
			if (false == index[i])
			{
				time_t tt = col[i];
				struct tm* ttime;
				ttime = localtime(&tt);
				ttimes[i] = tm_pt_2_tm_struct(ttime);
			}
		}
		for (vector<string>::iterator op = feaAttrib.operators.begin(); op != feaAttrib.operators.end(); op++)
		{
			FeatureAttribute outFeaAttrib;
			outFeaAttrib.name = feaAttrib.name + "_" + *op;
			outFeaAttrib.command = "timestamp";
			vector<int64_t> outFeature(ttimes.size());
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
		vector<int64_t> outFeature(col.size());
		for (size_t i = 0; i < col.size(); i++)
		{
			if (is_nan(col[i]))
			{
				index[i] = true;
			}
			if (false == index[i])
			{
				for (vector<double>::iterator it = feaAttrib.group_dists.begin(); it != feaAttrib.group_dists.end(); it++)
				{
					double grp_dist = *it;
					outFeature[i] = int64_t(col[i] * 1.0 / grp_dist);
				}
			}
			else {
				outFeature[i] = INT64_NAN;
			}
		}
		outFeaAttribs.push_back(feaAttrib);
		outFeatures.push_back(outFeature);
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
			if (is_nan(col[i]))
			{
				index[i] = true;
			}
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
				outFeaAttrib.command = "split";
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
				outFeaAttrib.command = "split";
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
				outFeaAttrib.command = "split";
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
				outFeaAttrib.command = "split";
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
				outFeaAttrib.command = "split";
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
	vector<T> col,
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
			string warning_str = "\nWarning!!! Labels have no such '";
			cout << warning_str << label << "' label!" << endl;
		}
	}
	return outFeatures;
}


template<typename T>
void _format_col(vector<T>& col, vector<bool>& index, FeatureAttribute feaAttrib) {
	for (size_t i = 0; i < col.size(); i++)
	{
		if (is_nan(col[i]))
		{
			index[i] = true;
		}
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
		if (is_nan(col[i]))
		{
			index[i] = true;
		}
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
vector<T> _count_col(vector<vector<int64_t>>& col_cnts, vector<int64_t>& target_nums, vector<int64_t>targets, vector<T> col) {
	vector<int64_t> target_keys;
	map<int64_t, int> target_map = vec_unique(targets, target_keys);
	sort(target_keys.begin(), target_keys.end());
	vector<int64_t> target_values = map_key_value(target_map, target_keys);

	vector<T> col_keys;
	map<T, int> col_map = vec_unique(col, col_keys);
	sort(col_keys.begin(), col_keys.end());
	vector<int64_t> col_values= map_key_value(col_map, col_keys);
	col_cnts.resize(col_keys.size());
	for (size_t i = 0; i < col_keys.size(); i++)
	{
		vector<T>keep_vals;
		vector<int>keep_idxs;
		vec_where(keep_vals, keep_idxs, col, col_keys[i]);
		vector<int64_t> keep_target = vec_keep(targets, keep_idxs);
		vector<int64_t> cnt(target_keys.size(), 0);
		for (size_t j = 0; j < target_keys.size(); j++)
		{
			vector<int64_t> keep_target_map_keys;
			map<int64_t, int> keep_target_map = vec_unique(keep_target, keep_target_map_keys);
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
	target_nums.resize(target_keys.size());
	for (size_t j = 0; j < target_keys.size(); j++)
	{
		target_nums[j] = target_keys[target_keys[j]];
	}
	return col_keys;
}
#endif // !REGION

/*================================================ Operator C++ <--> Python Transformation Module ===============================================*/
#ifndef REGION

vector<int64_t> PyList_AsVecInt(PyObject** pyList)
{
	Py_ssize_t pyList_size = PyList_Size(*pyList);
	vector<int64_t> vec(pyList_size);
	for (Py_ssize_t i = 0; i < pyList_size; ++i)
	{
		PyObject* obj = PyList_GetItem(*pyList, i);
		vec[i] = PyLong_Check(obj) ? PyLong_AsLongLong(obj) : INT64_MAX;
	}
	return vec;
}


PyObject* VecInt_AsPyList(vector<int64_t> vec)
{
	PyObject* pyList = PyList_New(vec.size());
	for (Py_ssize_t i = 0; i < vec.size(); ++i)
	{
		int ret = PyList_SetItem(pyList, i, Py_BuildValue("l", vec[i]));
	}
	return pyList;
}


PyObject* VecVecInt_AsPyList(vector<vector<int64_t>> vec)
{
	PyObject* pyList = PyList_New(vec.size());
	for (size_t i = 0; i < vec.size(); i++)
	{
		PyList_SetItem(pyList, i, VecInt_AsPyList(vec[i]));
	}
	return pyList;
}


vector<bool> PyList_AsVecBool(PyObject** pyList)
{
	Py_ssize_t pyList_size = PyList_Size(*pyList);
	vector<bool> vec(pyList_size);
	for (Py_ssize_t i = 0; i < pyList_size; ++i)
	{
		PyObject* obj = PyList_GetItem(*pyList, i);
		vec[i] = PyBool_Check(obj) ? PyLong_AsLong(obj) : true;
	}
	return vec;
}


PyObject* VecBool_AsPyList(vector<bool> vec)
{
	PyObject* pyList = PyList_New(vec.size());
	for (Py_ssize_t i = 0; i < vec.size(); ++i)
	{
		int ret = PyList_SetItem(pyList, i, Py_BuildValue("b", vec[i]));
	}
	return pyList;
}


PyObject* VecVecBool_AsPyList(vector<vector<bool>> vec)
{
	PyObject* pyList = PyList_New(vec.size());
	for (size_t i = 0; i < vec.size(); i++)
	{
		PyList_SetItem(pyList, i, VecBool_AsPyList(vec[i]));
	}
	return pyList;
}


vector<double> PyList_AsVecDouble(PyObject** pyList)
{
	Py_ssize_t pyList_size = PyList_Size(*pyList);
	vector<double> vec(pyList_size);
	for (Py_ssize_t i = 0; i < pyList_size; ++i)
	{
		PyObject* obj = PyList_GetItem(*pyList, i);
		vec[i] = PyFloat_Check(obj) ? PyFloat_AsDouble(obj) : NAN;
	}
	return vec;
}


PyObject* VecDouble_AsPyList(vector<double> vec)
{
	PyObject* pyList = PyList_New(vec.size());
	for (Py_ssize_t i = 0; i < vec.size(); ++i)
	{
		int ret = PyList_SetItem(pyList, i, Py_BuildValue("d", vec[i]));
	}
	return pyList;
}


PyObject* VecVecDouble_AsPyList(vector<vector<double>> vec)
{
	PyObject* pyList = PyList_New(vec.size());
	for (size_t i = 0; i < vec.size(); i++)
	{
		PyList_SetItem(pyList, i, VecDouble_AsPyList(vec[i]));
	}
	return pyList;
}


vector<string> PyList_AsVecStr(PyObject** pyList)
{
	Py_ssize_t pyList_size = PyList_Size(*pyList);
	vector<string> vec(pyList_size);
	for (Py_ssize_t i = 0; i < pyList_size; ++i)
	{
		PyObject* obj = PyList_GetItem(*pyList, i);
		vec[i] = PyUnicode_Check(obj) ? PyUnicode_AsUTF8(obj) : "";
	}
	return vec;
}


PyObject* VecStr_AsPyList(vector<string> vec)
{
	PyObject* pyList = PyList_New(vec.size());
	for (Py_ssize_t i = 0; i < vec.size(); ++i)
	{
		int ret = PyList_SetItem(pyList, i, Py_BuildValue("s", vec[i]));
	}
	return pyList;
}


PyObject* VecVecStr_AsPyList(vector<vector<string>> vec)
{
	PyObject* pyList = PyList_New(vec.size());
	for (size_t i = 0; i < vec.size(); i++)
	{
		PyList_SetItem(pyList, i, VecStr_AsPyList(vec[i]));
	}
	return pyList;
}


FeatureAttribute PyDict_AsFeaAttrib(PyObject** pyDict)
{
	FeatureAttribute feaAttrib;
	PyObject* pyDictKeys = PyDict_Keys(*pyDict);
	Py_ssize_t pyDictKeysLen = PyDict_Size(pyDictKeys);

	for (Py_ssize_t i = 0; i < pyDictKeysLen; ++i)
	{
		PyObject* key = PyList_GetItem(pyDictKeys, i);
		string key_str = PyUnicode_Check(key) ? PyUnicode_AsUTF8(key) : "";
		if ("name" == key_str)
		{
			PyObject* value = PyDict_GetItem(*pyDict, key);
			string val_str = PyUnicode_Check(key) ? PyUnicode_AsUTF8(key) : "";
			feaAttrib.name = val_str;
		}
		else if ("type" == key_str)
		{
			PyObject* value = PyDict_GetItem(*pyDict, key);
			string val_str = PyUnicode_Check(key) ? PyUnicode_AsUTF8(key) : "";
			feaAttrib.type = val_str;
		}
		else if ("transform" == key_str)
		{
			PyObject* value = PyDict_GetItem(*pyDict, key);
			string val_str = PyUnicode_Check(key) ? PyUnicode_AsUTF8(key) : "";
			feaAttrib.transform = val_str;
		}
		else if ("unit" == key_str)
		{
			PyObject* value = PyDict_GetItem(*pyDict, key);
			double t_val = PyFloat_Check(key) ? PyFloat_AsDouble(key) : NAN;
			feaAttrib.transform = t_val;
		}
		else if ("command" == key_str)
		{
			PyObject* value = PyDict_GetItem(*pyDict, key);
			string val_str = PyUnicode_Check(key) ? PyUnicode_AsUTF8(key) : "";
			feaAttrib.command = val_str;
		}
		else if ("operators" == key_str)
		{
			PyObject* value = PyDict_GetItem(*pyDict, key);
			for (size_t j = 0; j < PyTuple_Size(value); j++)
			{
				PyObject* item = PyTuple_GetItem(value, j);
				string val_str = PyUnicode_Check(item) ? PyUnicode_AsUTF8(item) : "";
				feaAttrib.operators.push_back(val_str);
			}
		}
		else if ("group_dists" == key_str)
		{
			PyObject* value = PyDict_GetItem(*pyDict, key);
			for (size_t j = 0; j < PyTuple_Size(value); j++)
			{
				PyObject* item = PyTuple_GetItem(value, j);
				double t_val = PyFloat_Check(item) ? PyFloat_AsDouble(item) : NAN;
				feaAttrib.group_dists.push_back(t_val);
			}
		}
		else if ("splits" == key_str)
		{
			PyObject* value = PyDict_GetItem(*pyDict, key);
			for (size_t j = 0; j < PyTuple_Size(value); j++)
			{
				PyObject* item = PyTuple_GetItem(value, j);
				string val_str = PyUnicode_Check(item) ? PyUnicode_AsUTF8(item) : "";
				feaAttrib.splits.push_back(val_str);
			}
		}
		else if ("index" == key_str)
		{
			PyObject* value = PyDict_GetItem(*pyDict, key);
			for (size_t j = 0; j < PyTuple_Size(value); j++)
			{
				PyObject* item = PyTuple_GetItem(value, j);
				int64_t val = PyLong_Check(item) ? PyLong_AsLongLong(item) : INT64_MAX;
				if (0 == j)
				{
					feaAttrib.start_index = val;
				}
				else if (1 == j)
				{
					feaAttrib.end_index = val;
				}
			}
		}
	}
	return feaAttrib;
}


PyObject* FeaAttrib_AsPyDict(FeatureAttribute feaAttrib)
{
	PyObject* pyDict = PyDict_New();

	PyDict_SetItem(pyDict, Py_BuildValue("s", "name"), Py_BuildValue("s", feaAttrib.name));
	PyDict_SetItem(pyDict, Py_BuildValue("s", "type"), Py_BuildValue("s", feaAttrib.type));
	PyDict_SetItem(pyDict, Py_BuildValue("s", "transform"), Py_BuildValue("s", feaAttrib.transform));
	PyDict_SetItem(pyDict, Py_BuildValue("s", "unit"), Py_BuildValue("d", feaAttrib.unit));
	PyDict_SetItem(pyDict, Py_BuildValue("s", "command"), Py_BuildValue("s", feaAttrib.command));
	PyDict_SetItem(pyDict, Py_BuildValue("s", "operators"), VecStr_AsPyList(feaAttrib.operators));
	PyDict_SetItem(pyDict, Py_BuildValue("s", "group_dists"), VecDouble_AsPyList(feaAttrib.group_dists));
	PyDict_SetItem(pyDict, Py_BuildValue("s", "splits"), VecStr_AsPyList(feaAttrib.splits));

	vector<int64_t> vec = { feaAttrib.start_index, feaAttrib.end_index };
	PyDict_SetItem(pyDict, Py_BuildValue("s", "index"), VecInt_AsPyList(vec));

	return pyDict;
}


PyObject* VecFeaAttrib_AsPyDict(vector<FeatureAttribute> vec)
{
	PyObject* pyList = PyList_New(vec.size());
	for (size_t i = 0; i < vec.size(); i++)
	{
		PyList_SetItem(pyList, i, FeaAttrib_AsPyDict(vec[i]));
	}
	return pyList;
}
#endif // !REGION

/*====================================================== Operator Python Module API ======================================================*/
#ifndef REGION

static PyObject* Operator_operator_col(PyObject* self, PyObject* args)
{
	PyObject* colObj, * feaAttribObj, * indexObj;
	if (!PyArg_ParseTuple(args, "OOO", &colObj, &feaAttribObj, &indexObj)) {
		return NULL;
	}
	FeatureAttribute feaAttrib = PyDict_AsFeaAttrib(&feaAttribObj);
	vector<bool> index = PyList_AsVecBool(&indexObj);
	if ("float" == feaAttrib.type)
	{
		vector<double> col = PyList_AsVecDouble(&colObj);
		vector < vector<int64_t>> outFeatures;
		vector < vector<bool>> outFeaIndexs;
		vector<FeatureAttribute> outFeaAttribs;
		_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecVecInt_AsPyList(outFeatures), VecFeaAttrib_AsPyDict(outFeaAttribs), VecVecBool_AsPyList(outFeaIndexs));
	}
	else if ("int" == feaAttrib.type)
	{
		vector<int64_t> col = PyList_AsVecInt(&colObj);
		vector < vector<int64_t>> outFeatures;
		vector < vector<bool>> outFeaIndexs;
		vector<FeatureAttribute> outFeaAttribs;
		_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecVecInt_AsPyList(outFeatures), VecFeaAttrib_AsPyDict(outFeaAttribs), VecVecBool_AsPyList(outFeaIndexs));
	}
	else if ("str" == feaAttrib.type || "" == feaAttrib.type)
	{
		vector<string> col = PyList_AsVecStr(&colObj);
		vector < vector<double>> outFeatures;
		vector<FeatureAttribute> outFeaAttribs;
		vector < vector<bool>> outFeaIndexs;
		_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecVecDouble_AsPyList(outFeatures), VecFeaAttrib_AsPyDict(outFeaAttribs), VecVecBool_AsPyList(outFeaIndexs));
	}
	PyErr_SetString(PyExc_TypeError, "int or str or fload type is expected!");
	return NULL;
}


static PyObject* Operator_col2feature(PyObject* self, PyObject* args)
{
	PyObject* colObj, * feaAttribObj, * indexObj, * labelsObj, * featureNamesObj, * featureValuesObj;
	if (!PyArg_ParseTuple(args, "OOOOOO", &colObj, &feaAttribObj, &indexObj, &labelsObj, &featureNamesObj, &featureValuesObj)) {
		return NULL;
	}
	FeatureAttribute feaAttrib = PyDict_AsFeaAttrib(&feaAttribObj);
	vector<bool> index = PyList_AsVecBool(&indexObj);
	vector<string> featureNames = PyList_AsVecStr(&featureNamesObj);

	Py_ssize_t pyList_size = PyList_Size(featureValuesObj);
	vector<vector<double>> featureValues(pyList_size);
	for (Py_ssize_t i = 0; i < pyList_size; ++i)
	{
		PyObject* obj = PyList_GetItem(featureValuesObj, i);
		featureValues[i] = PyList_AsVecDouble(&obj);
	}

	if ("float" == feaAttrib.type)
	{
		vector<double> col = PyList_AsVecDouble(&colObj);
		vector<double> labels = PyList_AsVecDouble(&labelsObj);
		vector<FeatureAttribute> outFeaAttribs;
		vector < vector<double>> outFeatures = _col2feature(outFeaAttribs, col, index, feaAttrib, labels, featureNames, featureValues);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecVecDouble_AsPyList(outFeatures), VecFeaAttrib_AsPyDict(outFeaAttribs), VecBool_AsPyList(index));
	}
	else if ("int" == feaAttrib.type)
	{
		vector<int64_t> col = PyList_AsVecInt(&colObj);
		vector<int64_t> labels = PyList_AsVecInt(&labelsObj);
		vector<FeatureAttribute> outFeaAttribs;
		vector < vector<double>> outFeatures = _col2feature(outFeaAttribs, col, index, feaAttrib, labels, featureNames, featureValues);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecVecDouble_AsPyList(outFeatures), VecFeaAttrib_AsPyDict(outFeaAttribs), VecBool_AsPyList(index));
	}
	else if ("str" == feaAttrib.type || "" == feaAttrib.type)
	{
		vector<string> col = PyList_AsVecStr(&colObj);
		vector<string> labels = PyList_AsVecStr(&labelsObj);
		vector<FeatureAttribute> outFeaAttribs;
		vector < vector<double>> outFeatures = _col2feature(outFeaAttribs, col, index, feaAttrib, labels, featureNames, featureValues);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecVecDouble_AsPyList(outFeatures), VecFeaAttrib_AsPyDict(outFeaAttribs), VecBool_AsPyList(index));
	}
	PyErr_SetString(PyExc_TypeError, "int or str or fload type is expected!");
	return NULL;
}


static PyObject* Operator_format_col(PyObject* self, PyObject* args)
{
	PyObject* colObj, * feaAttribObj, * indexObj;
	if (!PyArg_ParseTuple(args, "OOO", &colObj, &feaAttribObj, &indexObj)) {
		return NULL;
	}
	FeatureAttribute feaAttrib = PyDict_AsFeaAttrib(&feaAttribObj);
	vector<bool> index = PyList_AsVecBool(&indexObj);
	if ("float" == feaAttrib.type)
	{
		vector<double> col = PyList_AsVecDouble(&colObj);
		_format_col(col, index, feaAttrib);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecDouble_AsPyList(col), FeaAttrib_AsPyDict(feaAttrib), VecBool_AsPyList(index));
	}
	else if ("int" == feaAttrib.type)
	{
		vector<int64_t> col = PyList_AsVecInt(&colObj);
		_format_col(col, index, feaAttrib);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecInt_AsPyList(col), FeaAttrib_AsPyDict(feaAttrib), VecBool_AsPyList(index));
	}
	else if ("str" == feaAttrib.type || "" == feaAttrib.type)
	{
		vector<string> col = PyList_AsVecStr(&colObj);
		_format_col(col, index, feaAttrib);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecStr_AsPyList(col), FeaAttrib_AsPyDict(feaAttrib), VecBool_AsPyList(index));
	}
	PyErr_SetString(PyExc_TypeError, "int or str or fload type is expected!");
	return NULL;
}


static PyObject* Operator_count_col(PyObject* self, PyObject* args)
{
	PyObject* targetsObj, * colObj, * feaAttribObj;
	if (!PyArg_ParseTuple(args, "OOO", &targetsObj, &colObj, &feaAttribObj)) {
		return NULL;
	}
	vector<int64_t>targets = PyList_AsVecInt(&targetsObj);
	FeatureAttribute feaAttrib = PyDict_AsFeaAttrib(&feaAttribObj);
	if ("float" == feaAttrib.type)
	{
		vector<double> col = PyList_AsVecDouble(&colObj);
		vector<vector<int64_t>> col_cnts;
		vector<int64_t> target_nums;
		vector<double> labels = _count_col(col_cnts, target_nums, targets, col);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecDouble_AsPyList(labels), VecVecInt_AsPyList(col_cnts), VecInt_AsPyList(target_nums));
	}
	else if ("int" == feaAttrib.type)
	{
		vector<int64_t> col = PyList_AsVecInt(&colObj);
		vector<vector<int64_t>> col_cnts;
		vector<int64_t> target_nums;
		vector<int64_t> labels = _count_col(col_cnts, target_nums, targets, col);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecInt_AsPyList(labels), VecVecInt_AsPyList(col_cnts), VecInt_AsPyList(target_nums));
	}
	else if ("str" == feaAttrib.type || "" == feaAttrib.type)
	{
		vector<string> col = PyList_AsVecStr(&colObj);
		vector<vector<int64_t>> col_cnts;
		vector<int64_t> target_nums;
		vector<string> labels = _count_col(col_cnts, target_nums, targets, col);
		return (PyObject*)Py_BuildValue("(O,O,O)", VecStr_AsPyList(labels), VecVecInt_AsPyList(col_cnts), VecInt_AsPyList(target_nums));
	}
	PyErr_SetString(PyExc_TypeError, "int or str or fload type is expected!");
	return NULL;
}


int max(vector<int64_t> lst) {
	int max_num = INT_MIN;
	for (int i = 0; i < lst.size(); i++) {
		if (lst[i] > max_num) {
			max_num = lst[i];
		}
	}
	return max_num;
}

// 模块中每个可供Python调用的函数都需要一个对应的包裹函数
static PyObject* Operator_max(PyObject* self, PyObject* args) {
	PyObject* obj;
	// O代表对象
	if (!PyArg_ParseTuple(args, "O", &obj)) {
		return NULL;
	}

	vector<int64_t> lst = PyList_AsVecInt(&obj);
	return (PyObject*)Py_BuildValue("L", max(lst));
}

// 添加PyMethodDef ModuleMethods[]数组
static PyMethodDef OperatorMethods[] = {
	// add：可用于Python调用的函数名，Exten_add：C++中对应的函数名
	{"operator_col",Operator_operator_col,METH_VARARGS},
	{"col2feature",Operator_col2feature,METH_VARARGS},
	{"format_col",Operator_format_col,METH_VARARGS},
	{"count_col",Operator_count_col,METH_VARARGS},
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
#endif // !REGION


/*====================================================== Operator Test Module ======================================================*/
//#define TEST_FLAG
#ifdef TEST_FLAG

bool test_operator_col_double() {
	vector < vector<int64_t>> outFeatures;
	vector < vector<bool>> outFeaIndexs;
	vector<FeatureAttribute> outFeaAttribs;
	vector<double> col = { 1234567890 , 2234567890 };
	vector<bool> index = { false, false };
	FeatureAttribute feaAttrib;

	feaAttrib.name = "testName";
	feaAttrib.command = "None";
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);

	feaAttrib.command = "timestamp";
	feaAttrib.operators = { "sec" , "min", "hour","mday" ,"mon" ,"year" ,"wday" ,"yday" ,"isdst"};
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);

	feaAttrib.command = "group";
	feaAttrib.group_dists = { 2,5,0.2 };
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
	printf("\ntest_operator_col_double () test ok!\n");
	return true;
}


bool test_operator_col_string() {
	vector < vector<double>> outFeatures;
	vector < vector<bool>> outFeaIndexs;
	vector<FeatureAttribute> outFeaAttribs;
	vector<string> col = { "a:3.4|b:6.5" , "abb:56.62234567890|bbb:" };
	vector<bool> index = { false, false };
	FeatureAttribute feaAttrib;

	feaAttrib.name = "testName";
	feaAttrib.command = "split";
	feaAttrib.operators = { "len","sum","mean","max","min" };
	feaAttrib.splits = { "|",":"};
	feaAttrib.group_dists = { 2,5,0.2,5,0.5 };
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);

	col = { "[app_1 ]" , "" };
	feaAttrib.command = "split";
	feaAttrib.operators = { "len" };
	feaAttrib.splits = { " " };
	feaAttrib.group_dists = { 2};
	feaAttrib.start_index = 1;
	feaAttrib.end_index = -2;
	_operator_col(outFeatures, outFeaIndexs, outFeaAttribs, col, index, feaAttrib);
	printf("\ntest_operator_col_string () test ok!\n");
	return true;
}


bool test_col2feature() {
	vector<FeatureAttribute> outFeaAttribs;
	vector<string> col = { "1","2","3" };
	vector<bool> index = { false,false,false };
	FeatureAttribute feaAttrib;
	vector<string> labels = { "1","2" };
	vector<string> featureNames = { "A","B","C" };
	vector<vector<double>> featureValues(3);

	feaAttrib.name = "testName";
	featureValues[0] = {0,1};
	featureValues[1] = { 2,3 };
	featureValues[2] = { 4,5 };
	vector < vector<double>> result = _col2feature(outFeaAttribs, col, index, feaAttrib, labels, featureNames, featureValues);
	printf("\ntest_col2feature () test ok!\n");
	return true;
}



bool test_count_col() {
	vector<vector<int64_t>> col_cnts;
	vector<int64_t> target_nums;
	vector<int64_t>targets = { 1,1,1,0,1,0,0 };
	vector<int64_t> col = { 1,1,2,5,7,3,7};
	vector<int64_t> keys = _count_col(col_cnts, target_nums, targets, col);
	printf("\ntest_count_col () test ok!\n");
	return true;
}
int main(int argc, char* argv[])
{
	test_operator_col_double();
	test_operator_col_string();
	test_col2feature();
	test_count_col();

	Py_SetPythonHome(L"D:\\Install\\Anaconda3");
	Py_Initialize();
	PyRun_SimpleString("import sys");
	PyRun_SimpleString("sys.path.append('./')");

	PyObject* pModule;
	PyObject* py_func;
	pModule = PyImport_ImportModule("cal");
	py_func = PyObject_GetAttrString(pModule, "mix");
	PyObject* py_ret_value = PyObject_CallFunction(py_func, NULL);

	vector<double> vec_double = PyList_AsVecDouble(&py_ret_value);
	vector<string> vec_str = PyList_AsVecStr(&py_ret_value);
	vector<int64_t> vec_int = PyList_AsVecInt(&py_ret_value);

	Py_Finalize();
	return 0;
}


#endif // TEST_FLAG

#endif // !__UTILS_MODULE_CPP
