#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

vector<string> readTxt();
void out2txt(vector<string> sOut);

int main()
{
    vector<string> timeTags;
    int timeDis = 0;     //读取txt文件时，如果发现文件被修改，置为0，否则开始累加
    int countBag = 0;
    //read mktdt00.txt and return a string array
    vector<string> sIn;
    string preTimeStr = "";  //上一个阶段 txt文件中的时间戳
    while(timeDis<100)    //累加到20就认为文件不会被修改
    {
        sIn = readTxt();      //读取文本成为字符串数组
        //get time in each mktdt00.txt
        string tmpStr=sIn[0];
        int timeStrPos0 = 0,timeStrPos1=0;   //时间戳字符串起始时间

        timeStrPos0 = tmpStr.find("XSHG01")+16;
        timeStrPos1 = tmpStr.find("|",timeStrPos0);
        string timeStr = tmpStr.substr(timeStrPos0,timeStrPos1-timeStrPos0);
        if(preTimeStr.size()==0)
        {
            preTimeStr = timeStr;
        }
        if(timeStr != preTimeStr)
        {
            countBag++;   //文件被修改 ，数据包计数+1
            cout<<"dataBagID : "<<countBag<<"\t"<<"Time :  "<<timeStr<<endl;
            timeTags.push_back(timeStr);
            timeDis = 0;
            preTimeStr=timeStr;
        }
        sIn.clear();
        _sleep(1000);
        timeDis++;
    }
    cout<<"timeDis = "<<timeDis<<endl;

    //output result to txtfile
    out2txt(timeTags);

    cout << "Hello world!" << endl;
    return 0;
}

vector<string> readTxt()
{
    vector<string> res;
    ifstream openf("filename.txt",ios::in);
    if(!openf.is_open())
    {
        cout<<" error in open txt file! "<<endl;
        exit(-1);
    }
    int count=0;
    string str="";
    while(getline(openf,str))
    {
        //cout<<str<<endl;
        res.push_back(str);
        count++;
        if(count>20) break;
    }
    return res;
}

void out2txt(vector<string> sOut)
{
    ofstream resOut("resultOut.txt",ios::out);
    if(!resOut)
    {
        cerr<<"fail to open file 'resOut.txt'"<<endl;
        exit(-1);
    }
    for(int i=0;i<sOut.size();++i)
    {
        resOut<<sOut[i]<<endl;
    }
    resOut.close();
}


