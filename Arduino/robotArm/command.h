#ifndef COMMAND_H_
#define COMMAND_H_

#include <Arduino.h>

struct Cmd {
  char id;
  int num;
  float valueX;
  float valueY;
  float valueZ;
  float valueF;
  float valueE;
  float valueT; 
};



class Command {
  public:
    Command();
    
    static const byte numChars = 32;
    char receivedChars[numChars];   // an array to store the received data
    
    bool handleGcode();
    bool processMessage(String& msg);
    Cmd getCmd() const;
    String message;
    
    
  
  private: 
    int pos(String& s, char c, int start = 0);
    
    Cmd command;
};

void printErr();
void printFault();
void printComment(char* c);
void printComment(String& s);
void printOk();


#endif
