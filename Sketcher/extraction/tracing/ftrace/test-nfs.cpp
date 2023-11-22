// test file I/O through user-level function
#include <iostream>
#include <fstream>
#include <time.h>

// add for ftrace
#include <stdio.h>
//#include <io.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
using namespace std;

int main(){
	//get current pid
	pid_t pid;
	pthread_t tid;
	pid=getpid();
	tid=pthread_self();
	printf("pid %u tid %u (0x%x)\n",(unsigned int)pid, (unsigned int)tid, (unsigned int)tid);
	//deliver flag and pid to the server
	int flag_ofs=open("/backups/FLAG", O_RDWR+O_CREAT);
	char pid_char[30];
	sprintf(pid_char, "1, %u",(unsigned int)pid);
	int flag_len= write(flag_ofs,pid_char,strlen(pid_char));	
	printf("flag len sent: %d\n", flag_len);
	close(flag_ofs);

	// define for ftrace
	//int fd_sched = open("/sys/kernel/debug/tracing/events/sched/enable",O_CREAT | O_RDWR, 0666);
	//int fd_irq =   open("/sys/kernel/debug/tracing/events/irq/enable", O_CREAT | O_RDWR, 0666);
	
	int fd_nfs = open("/sys/kernel/debug/tracing/events/nfs4/enable",O_CREAT | O_RDWR, 0666);
	//int fd_rpc =   open("/sys/kernel/debug/tracing/events/rpcgss/enable", O_CREAT | O_RDWR, 0666);
	
	
	int fd_mark  = open("/sys/kernel/debug/tracing/trace_marker", O_CREAT | O_RDWR, 0666);
	int fd_trace = open("/sys/kernel/debug/tracing/tracing_on", O_CREAT | O_RDWR, 0666);
	int fd_cur   = open("/sys/kernel/debug/tracing/current_tracer", O_CREAT | O_RDWR,0666);
	//int fd_enab  = open("/sys/block/sde/sde1/trace/enable", O_CREAT | O_RDWR,0666);
	
	write(fd_trace, "1", 2);
	
	write(fd_nfs, "1", 2);
	//write(fd_rpc,"1", 2);
	write(fd_cur,"function_graph",20);
	//write(fd_enab,"1",2);
	// start marker
	write(fd_mark, "start test", 12);
	
	//my code
	//srand((unsigned)time(NULL));
	
	//write(fd_mark, "initial data[100]\n", 12);
	char data[200]={" test write to NFS, now we can make some difference:\n"};
	char digit[100];
//	for (int i=0;i<20;i++){
//		digit[i]=rand()%10-'0';
//	}

	//write(fd_mark,"end initial data[100]\n",12);	
	
	//ofstream outfile;
	//write(fd_mark,"end initial ofs",12);
	//int ofs=open("/media/nas/hkc/localopenNAS-2.txt", O_RDWR+O_CREAT);
	int ofs=open("/backups/localopenNAS-1.txt", O_RDWR+O_CREAT);
	//outfile.open("/home/hkc/tracer/trace-cmds/localfile.txt");

	//int ofs=open("/home/hkc/tracer/localfile.txt", O_RDWR+O_CREAT);
		
		
	//write(fd_mark, "end open ofs", 12);

	//cout << "Input char:"<<endl;
	//write(fd_mark,"end input char",20);	

	//cin.getline(data,100);
	//write(fd_mark,"end getline",20);	
	
	
	for (int i=0;i<1;i++){
		//outfile << "hkc123-";
		//outfile << data <<endl;
		//write(fd_mark,"Start write hkc to ofs.\n",30);
		//outfile << i;
		//outfile << " ";
		//outfile << rand()%100+1 <<endl;
		sprintf(digit, "%d %d %d %d\n", rand()%10000000, rand()%10000000, rand()%10000000, rand()%10000000);
		//write(fd_mark,"start.\n",10);	
		int len1=write(ofs,data,strlen(data));
		int len2=write(ofs,digit,strlen(digit));
		//write(fd_mark,"end. \n",10);
		printf("%d-th input len1 = %d; len2 = %d. \n",i,len1,len2);
	}

	//outfile << data <<endl;
	//write(fd_mark,"Start write hkc to ofs.\n",20);
	//outfile << "hkc" <<endl;
	//write(fd_mark,"1#: end write hkc to ofs.\n",20);
	
	//cout <<"please input next char:"<<endl;
	//write(fd_mark,"end inform cout",12);	
	
	//cin>> data;
	//write(fd_mark,"end cin",12);	
	
	//cin.ignore();
	//write(fd_mark,"end cin ignore",12);	
	
	//outfile << data <<endl;
	//write(fd_mark,"2#: end write data to ofs",20);	
	
	//outfile.close();
	close(ofs);
	//write(fd_mark,"end close ofs\n",20);	
	//end of my code

	//end marker
	write(fd_mark,"end test",12);

	//disable ftrace
	write(fd_trace,"0",2);
	//write(fd_enab,"0",2);
	write(fd_nfs,"0",2);
	//write(fd_rpc, "0",2);

	//close all pointer
	close(fd_mark);
	close(fd_trace);
	close(fd_cur);
	//close(fd_enab);
	close(fd_nfs);
	//close(fd_rpc);


	return 0;
}
