#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>

using namespace std;

void split(string str,vector<string>& res);
vector<string> readTxt();
int getCol(string timeStr);
bool checkTime(string timess);

int main() {
	
	//read resOut.txt and build Array
	vector<string> lines;
	lines = readTxt();
	
	vector<vector<string> > resOut;
	vector<string> tmp;
	for(int i=0;i<lines.size();++i)
	{
		split(lines[i],tmp);
		resOut.push_back(tmp);
		tmp.clear();
	}
	
	//build dictionay of (ID,index)
	unordered_map<string,int> mapping;
	for(int i=0;i<resOut.size();++i)
	{
		string id = resOut[i][0].substr(0,6);
		mapping[id]=i;
	}
	
	//search
	string id = "";
	string timess ="";
	cout<<"please input SecurityID and Time : (input 'end' to exit !)"<<endl;
	cout<<"such as : 600178 09:35 "<<endl;
	cout<<"--------------------------------------------"<<endl;
	while(id!="end")
	{
		cin>>id;
		if(id == "end") break;
		cin>>timess;
		if(timess == "end") break;
		//check id
		if(mapping.find(id)!=mapping.end())
		{
		 	int index=mapping[id];
		 	
		 	//check time
			int col = getCol(timess);
			while(col == -1) 
			{
				cout<<"timess is not a normal value,input time again."<<endl;
				cin>>timess;
				col = getCol(timess);
				if(timess == "end") exit(0);
			}	
			
			// start to analyze and search
			string idAndName = resOut[index][0]; 
			string resStr = resOut[index][col];
			cout<<"SecurityID : "<<id<<endl;
			cout<<"Symbol : "<<idAndName.substr(7,idAndName.size()-7)<<endl;
			//find pos function() need to be cheacked......
			/*
			some resStr="0"
			*/
			int pos = resStr.find('|',6);
			if(pos != string::npos)
			{
				cout<<"Price  : "<<resStr.substr(6,resStr.find('|',6)-6)<<endl;
				cout<<"Volume : "<<resStr.substr(resStr.find('|',6)+1)<<endl;
			}
			else
			{
				cout<<"data in this position was wrong !"<<endl;
				cout<<"the string was : "<<resStr<<endl;
			}
			
		}
		else
		{
			cout<<"this SecurityID was not in dataBase ! PLZ input another one!"<<endl;
		}
		
		cout<<"--------------------------------------------"<<endl;
		cout<<"please input SecurityID and Time : "<<endl;
		
	}
	
	return 0;
	
}

void split(string str,vector<string>& res)
{
    if(str.empty())
    {
        return;
    }
    int pos0=0;
    for(int i=0;i<=str.size();++i)
    {
        if(str[i]==',' || str[i]=='\0')
        {
            res.push_back(str.substr(pos0,i-pos0));
            pos0=i+1;
        }
    }
}

vector<string> readTxt()
{
    vector<string> res;
    ifstream openf("resOut.txt",ios::in);
    if(!openf.is_open())
    {
        cout<<" error in open txt file! "<<endl;
        exit(-1);
    }
    string str="";
    while(getline(openf,str))
    {
        //cout<<str<<endl;
        res.push_back(str);
    }
    return res;
}

int getCol(string timeStr)
{
	//check time
	if(timeStr.size()>5 || timeStr.size()<4)
	{
		return -1;
	}
	
	if(timeStr.size()==4) timeStr = '0'+timeStr;
	for(int i=0;i<5;++i)
	{
		if(::isdigit(timeStr[i]))
		{
			continue;
		}
		else if((!::isdigit(timeStr[i])) && i==2)
		{
			continue;
		}
		else return -1;
	}
	
    int hour = atoi(timeStr.substr(0,2).c_str());
    int minutes = atoi(timeStr.substr(3,2).c_str());
    if(minutes>=60) return -1;
    int num = hour*100+minutes;
    if(num>=931 && num<=1130)
    {
        return (hour-9)*60+minutes-30;
    }
    else if(num>=1301 && num<=1500)
    {
        return 120+(hour-13)*60+minutes;
    }
    else return -1;

}
