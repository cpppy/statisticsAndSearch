#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

vector<string> readTxt();
string time2hm(string timeStr);
int getCol(string timeStr);
void restoreResult(vector<vector<string> > resOut);
string delSpace(string s);


int main()
{
    vector<string> timeTags;
    vector<vector<string> > resOut(1173,vector<string>(241,"0"));
    vector<vector<string> > preMinVol(1173,vector<string>(3,"0"));
    vector<vector<string> > preData(1173,vector<string>(4,"0"));



    int IDindex=0;
    int timeDis = 0;     //读取txt文件时，如果发现文件被修改，置为0，否则开始累加
    int countBag = 0;

    //read mktdt00.txt and return a string array
    vector<string> sIn;

    string preTimeStr = "";  //上一个阶段 txt文件中的时间戳

    while(timeDis<100)    //累加到100就认为文件不会再被修改，整个过程结束
    {
        sIn = readTxt();      //读取文本成为字符串数组
        if(sln.size()==0) 
        {
            cout<<"array from readTXT() was empty!"<<endl;
            break;
        }

       //获得文本中第一行里的时间，用以判断文本是否被修改
        string tmpStr=sIn[0];
        int timeStrPos0 = 0,timeStrPos1=0;   //时间戳字符串起始时间
        timeStrPos0 = tmpStr.find("XSHG01")+16;
        timeStrPos1 = tmpStr.find("|",timeStrPos0);
        if(timeStrPos0 != string::npos && timeStrPos1 != string::npos)
        {
            string timeStr = tmpStr.substr(timeStrPos0,timeStrPos1-timeStrPos0);
        }
        else 
        {
            cout<<"Not Found timeStrPos, can not get timeStr ! "<<endl;
        }
        

        //初始化 preTimeStr , 并将股票的ID 和 中文简称 写入数组中
        if(preTimeStr.size()==0)
        {
            preTimeStr = timeStr;
            int index=0;
            for(int i =1;i<sIn.size()-1;++i)
            {
                tmpStr = sIn[i];
                //find "MD002",if it is, get Trade Volume and Price
                if(tmpStr[4]=='2')
                {
                    string idAndName = tmpStr.substr(6,tmpStr.find("|",13)-6);
                    idAndName = delSpace(idAndName);
                    resOut[index][0] = idAndName;
                    index++;
                }
            }
        }

        if(timeStr != preTimeStr)    //判断文件是否被修改
        {
            countBag++;   //文件被修改 ，数据包计数+1
            cout<<"dataBagID : "<<countBag<<"\t"<<"HeadTime :  "<<timeStr<<endl;
            //string timeOutTag = "dataBagID : "+to_string(countBag)+"\t"+"Time :  "+timeStr;
            //timeTags.push_back(timeOutTag);
            timeDis = 0;    //发现新包，计时器清零
            preTimeStr=timeStr;

            //处理 sIn 数组中的数据
            for(int i =1;i<sIn.size()-1;++i)
            {
                tmpStr = sIn[i];
                //find "MD002",if it is, get Trade Volume and Price
                if(tmpStr[4]=='2')
                {
                    //get Trade Volume
                    string volss = tmpStr.substr(22,tmpStr.find('|',23)-22);
                    //cout<<atoi(volss.c_str())<<endl;

                    //get time and price
                    int pos = tmpStr.find_first_of("TPBESC"，50); 
            
                    string timess = tmpStr.substr(pos+9,12);
                    string pricess = tmpStr.substr(pos-25,11);
                    //cout<<pricess<<'\t'<<timess<<endl;

                    //statistic and restore
                    if(time2hm(timess) != preData[IDindex][1] && getCol(timess)>0)    //当本次时间的分钟发生改变时，则选取preData的数据作为上一分钟的数据写入resOut中
                    {
                        int col = getCol(timess);
                        long long quantity = atoi((preData[IDindex][3]).c_str()) - atoi((preMinVol[IDindex][2]).c_str());

                        string outss = preData[IDindex][1]+'|'+delSpace(preData[IDindex][2])+'|'+to_string(quantity);
                        resOut[IDindex][col] = outss;
                        outss.clear();

                        // preMinVol 的数据修改为上一分钟末尾时的时间和Trade Volume
                        preMinVol[IDindex][2] = preData[IDindex][3];
                        preMinVol[IDindex][1] = preData[IDindex][1];
                        // preData 读取本次的新分钟的开始数据
                        preData[IDindex][1] = time2hm(timess);
                        preData[IDindex][2] = pricess;
                        preData[IDindex][3] = volss;

                    }
                    else
                    {
                        //仍然在当前分钟内，只需更新preData 中的数据即可
                        preData[IDindex][1] = time2hm(timess);
                        preData[IDindex][2] = pricess;
                        preData[IDindex][3] = volss;
                    }
                    IDindex++;
                    if(IDindex>1172) 
                    {
                        cout<<"IDindex = "<<IDindex<<"\t"<<"new MD002 come out"<<endl;
                        cout<<tmpStr<<endl;
                        break;
                    }
                }
            }
            IDindex=0;


        }

        sIn.clear();
        _sleep(1000);
        timeDis++;

        //if(countBag>300) break;

    }

    cout<<"timeDis = "<<timeDis<<endl;
    restoreResult(resOut);

    //output result to txtfile
    //out2txt(timeTags);

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
    //int count=0;  //读取行数
    string str="";
    while(getline(openf,str))
    {
        //cout<<str<<endl;
        res.push_back(str);
        //count++;
        //if(count>20) break;
    }
    return res;
}

string time2hm(string timeStr)
{
    return timeStr.substr(0,5);
}

int getCol(string timeStr)
{
    if(timeStr.size()<12) return -1;
    int hour = atoi(timeStr.substr(0,2).c_str());
    int minutes = atoi(timeStr.substr(3,2).c_str());
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

void restoreResult(vector<vector<string> > resOut)
{
    ofstream outf("resOut.txt",ios::out);
    if(!outf)
    {
        cerr<<"fail to open file 'resOut.txt'"<<endl;
        exit(-1);
    }
    for(int i=0;i<resOut.size();++i)
    {
        for(int j=0;j<resOut[0].size();++j)
        {
            outf<<resOut[i][j]<<',';
        }
        outf<<endl;
    }
    outf.close();

}

string delSpace(string s)
{
    int i=0;
    while(s[i]==' ')
    {
        i++;
    }
    s = s.substr(i,s.size()-i);

    int j=s.size()-1;
    while(s[j]==' ')
    {
        j--;
    }
    s = s.substr(0,j+1);
    return s;
}



