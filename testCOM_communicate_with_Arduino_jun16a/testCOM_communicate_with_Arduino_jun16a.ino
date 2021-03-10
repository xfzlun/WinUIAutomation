
void setup(){
   Serial.begin(9600); // 9600波特率
}

void loop() {
   if ( Serial.available())//判断串口缓存区有没有数据
    {
      if('s' == Serial.read())//有数据就用read来读取并判断是不是s
        Serial.println("Hello Raspberry,I am Laurence's Arduino.");//是的话就向串口打印这串字符
     }
}

