#include<iostream>
#include<stdio.h>
#include<string.h>
//for pthread
#include <unistd.h>
//for file IO
#include <sys/types.h> 
#include <sys/stat.h>    
#include <fcntl.h>

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



	//start ftrace
	FILE *op=NULL;
	char startFt[100];
	char endFt[100];
	char addMark[100];
	sprintf(startFt,"/home/hkc/test/tracer-sh/ftOpen.sh");
	sprintf(endFt,"/home/hkc/test/tracer-sh/ftClose.sh");
	sprintf(addMark,"/home/hkc/test/tracer-sh/addMark.sh");
	op=popen(startFt,"r");
	pclose(op);
	op=NULL;
	
	//add mark
	int fd_mark  = open("/tracing/trace_marker", O_CREAT | O_RDWR, 0666);
	write(fd_mark, "hkc start test", 12);



	/*Code logic*/	
	char data[200]={" test write to NFS, now we can make some difference:\n"};
	char digit[100];
	int ofs=open("/backups/localopenNAS-1.txt", O_RDWR+O_CREAT);
	for (int i=0;i<1000;i++){
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
	close(ofs);
	
	/*End of Code logic*/
	write(fd_mark, "hkc end test", 12);
	close(fd_mark);
	
	//end ftrace
	op=popen(endFt,"r");
	pclose(op);
	op=NULL;
	
	cout <<"OK"<<endl;
	return 0;

}
