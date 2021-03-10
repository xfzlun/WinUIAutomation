# USB HID 单片机实现Study note

HID是一種USB通訊協議，無需安裝驅動就能進行互動，這給手持搖桿手柄類的遊戲開發提供了便利。順便說一下，手持搖桿類遊戲也支援安卓和蘋果手機



**USB裝置描述符－概述**

當插入USB裝置後，主機會向裝置請求各種描述符來識別裝置。那什麼是裝置描述符呢？

Descriptor即描述符，是一個完整的資料結構，可以通過C語言等程式設計實現，並存儲在USB裝置中，用於描述一個USB裝置的所有屬性，USB主機是通過一系列命令來要求裝置傳送這些資訊的。

描述符的作用就是通過命令操作作來給主機傳遞資訊，從而讓主機知道裝置具有什麼功能、屬於哪一類裝置、要佔用多少頻寬、使用哪類傳輸方式及資料量的大小，只有主機確定了這些資訊之後，裝置才能真正開始工作。

USB有那些標準描述符？ 

USB有5種標準描述符：裝置描述符 、配置描述符、字元描述符、介面描述符、端點描述符 。

描述符之間有一定的關係，一個裝置只有一個裝置描述符，而一個裝置描述符可以包含多個配置描述符，而一個配置描述符可以包含多個介面描述符，一個介面使用了幾個端點，就有幾個端點描述符。由此我們可以看出，USB的描述符之間的關係是一層一層的，最上一層是裝置描述符，下面是配置描述符，再下面是介面描述符，再下面是端點描述符。在獲取描述符時，先獲取裝置描述符，然後再獲取配置描述符，根據配置描述符中的配置集合長度，一次將配置描述符、介面描述符、端點描述符一起一次讀回。其中可能還會有獲取裝置序列號，廠商字串，產品字串等。

裝置描述符

```
struct _DEVICE_DEscriptOR_STRUCT
{
 BYTE  bLength;  //裝置描述符的位元組數大小
 BYTE  bDescriptorType;  //描述符型別編號，為0x01
 WORD bcdUSB;  //USB版本號
 BYTE bDeviceClass;  //USB分配的裝置類程式碼，0x01~0xfe為標準裝置類，0xff為廠商自定義型別，0x00不是在裝置描述符中定義的，如HID
 BYTE  bDeviceSubClass; //usb分配的子類程式碼，同上，值由USB規定和分配的，HID裝置此值為0
 BYTE bDeviceProtocl; //USB分配的裝置協議程式碼，同上HID裝置此值為0
 BYTE  bMaxPacketSize0; //端點0的最大包的大小
 WORD  idVendor; //廠商編號
 WORD  idProduct; //產品編號
 WORD bcdDevice; //裝置出廠編號
 BYTE  iManufacturer;  //描述廠商字串的索引
 BYTE  iProduct;  //描述產品字串的索引
 BYTE  iSerialNumber; //描述裝置序列號字串的索引
 BYTE  bNumConfiguration;  //可能的配置數量
}

配置描述符 
struct _CONFIGURATION_DEscriptOR_STRUCT

{
 BYTE bLength;  //配置描述符的位元組數大小
 BYTE  bDescriptorType;  //描述符型別編號，為0x02
 WORD  wTotalLength;  //配置所返回的所有數量的大小
 BYTE  bNumInterface; //此配置所支援的介面數量
 BYTE  bConfigurationVale;  //Set_Configuration命令需要的引數值
 BYTE  iConfiguration; //描述該配置的字串的索引值
 BYTE bmAttribute; //供電模式的選擇
 BYTE  MaxPower;  //裝置從匯流排提取的最大電流

}

字元描述符 
struct _STRING_DEscriptOR_STRUCT

{

BYTE bLength; //字串描述符的位元組數大小
BYTE bDescriptorType; //描述符型別編號，為0x03
BYTE SomeDescriptor[36]; //UNICODE編碼的字串

}

介面描述符

struct _INTERFACE_DEscriptOR_STRUCT

{

BYTE bLength; //介面描述符的位元組數大小

BYTE bDescriptorType; //描述符型別編號，為0x04

BYTE bInterfaceNunber; //介面的編號

BYTE bAlternateSetting;//備用的介面描述符編號

BYTE bNumEndpoints; //該介面使用端點數，不包括端點0

BYTE bInterfaceClass; //介面型別 HID裝置此值為0x03

BYTE bInterfaceSubClass;//介面子型別 HID裝置此值為0或者1

BYTE bInterfaceProtocol;//介面所遵循的協議

BYTE iInterface; //描述該介面的字串索引值

}

端點描述符

struct _ENDPOIN_DEscriptOR_STRUCT

{

BYTE bLength; //端點描述符的位元組數大小

BYTE bDescriptorType; //描述符型別編號，為0x05

BYTE bEndpointAddress; //端點地址及輸入輸出屬性

BYTE bmAttribute; //端點的傳輸型別屬性

WORD wMaxPacketSize; //端點收、發的最大包的大小

BYTE bInterval; //主機查詢端點的時間間隔

}
```



**HID裝置描述符**

溫習了以上內容，我們再來看看HID協議與這些描述符之間的關係。

當插入USB裝置後，主機會向裝置請求各種描述符來識別裝置。

為了把一個裝置識別為HID類別，裝置在定義描述符的時候必須遵守HID規範。

![img](http://hi.csdn.net/attachment/201108/26/0_13143288015H7B.gif)

從框圖中，可以看出除了USB標準定義的一些描述符外，HID裝置還必須定義HID描述符。另外裝置和主機的通訊是通過報告的形式來實現的，所以還必須定義報告描述符；而物理描述符不是必需的。還有就是HID描述符是關聯於介面（而不是端點）的，所以裝置不需要為每個端點都提供一個HID描述符。

介面描述符中bInterfaceClass的值必須為0x03，bInterfaceSubClass的值為0或1，為1表示HID裝置符是一個啟動裝置（Boot Device，一般對PC機而言才有意義，意思是BIOS啟動時能識別並使用您的HID裝置，且只有標準滑鼠或鍵盤類裝置才能成為Boot Device。如果為0則只有在作業系統啟動後才能識別並使用您的HID裝置）。

| **USB HID類描述符的結構** |                   |      |      |                                                              |
| ------------------------- | ----------------- | ---- | ---- | ------------------------------------------------------------ |
| 偏移量                    | 域                | 大小 | 值   | 描述                                                         |
| 0                         | bLength           | 1    | 數字 | 此描述符的長度（以位元組為單位）                             |
| 1                         | bDescriptorType   | 1    | 常量 | 描述符種類（此處為0x21即HID類描述符）                        |
| 2                         | bcdHID            | 2    | 數字 | HID規範版本號（BCD碼），採用4個16進位制的BCD格式編碼，如版本1.0的BCD碼為0x0100,版本為1.1的BCD碼為0x0110 |
| 4                         | bCountryCode      | 1    | 數字 | 硬體目的國家的識別碼（BCD碼）（見表3）                       |
| 5                         | bNumDescritors    | 1    | 數字 | 支援的附屬描述符數目                                         |
| 6                         | bDescriptorType   | 1    | 常量 | HID相關描述符的型別0x21：HID描述符0x22：報告描述符0x23：物理描述符 |
| 7                         | wDescriptorLength | 2    | 數字 | 報告描述符總長度                                             |
| 9                         | bDescriptorType   | 1    | 常量 | 用於識別描述符型別的常量，使用在有一個以上描述符的裝置       |
| 10                        | wDescriptorLength | 2    | 數字 | 描述符總長度，使用在有一個以上描述符的裝置                   |

**報告描述符**

報告描述符比較複雜，它是以item形式排列組合而成，無固定長途，使用者可以自定義長度以及每一bit的含義。item型別分三種：main，global和local，其中main型別又可分為5種tag：

- input item tag：指的是從裝置的一個或多個類似控制管道得到的資料
- output item tag：指的是傳送給一個或多個類似控制管道的資料
- feature item tag：表示裝置的輸入輸出不面向終端使用者
- collection item tag：一個有意義的input，output和feature的組合專案
- end collection item tag：指定一個collectionitem的終止

每一個main item tag（input，output，feature）都表明了來自一個特定管道的資料的大小，資料相對還是獨立，以及其他相關資訊。在此之前，global和local item定義了資料的最大值和最小值，等等。local item僅僅描述下一個main item定義的資料域，而global item是這一個報告描述符中所有後續資料段的預設屬性。

 一個報告描述符可能包含多個main item，為了準確描述來自一個控制管道的資料，一個報告描述符必須包括以下內容：

- input（output，feature）
- usage
- usage page
- Logical Minimum
- Logical Maximum
- Report Size
- Report Count

下面用一個三鍵滑鼠舉例說明：

Usage Page (Generic Desktop);  //global item

Usage (Mouse);  //global item 
Collection (Application);  //Start Mouse collection
Usage (Pointer);  //
Collection (Physical);  //Start Pointer collection
Usage Page (Buttons)
Usage Minimum (1),
Usage Maximum (3),
Logical Minimum (0),
Logical Maximum (1) ;  //Fields return values from 0 to 1
Report Count (3),
Report Size (1);  //Create three 1 bit fields (button 1, 2, & 3)
Input (Data, Variable, Absolute);  //Add fields to the input report.
Report Count (1),
Report Size (5);  //Create 5 bit constant field
Input (Constant), ;Add field to the input report
Usage Page (Generic Desktop),
Usage (X),
Usage (Y),
Logical Minimum (-127),
Logical Maximum (127);  //Fields return values from -127 to 127
Report Size (8),
Report Count (2);  //Create two 8 bit fields (X & Y position)
Input (Data, Variable, Relative);  //Add fields to the input report
End Collection;  //Close Pointer collection
End Collection;  //Close Mouse collection

item的資料格式有兩種，分別是短item和長item。

短item格式

![](https://raw.githubusercontent.com/xfzlun/xfzlun.github.iogithub/master/%E6%88%AA%E5%B1%8F2020-08-26%20%E4%B8%8B%E5%8D%884.43.01.png)



| bSize | 0：0個位元組. 1：1個位元組.  2：2個位元組.  3：4個位元組     |
| ----- | ------------------------------------------------------------ |
| bType | 0：main. 1：global.  2：local.  3：保留                      |
| bTag  | item型別.  8：input.   9：output.   A：collection.   B：feature.   C：end collection |

長item，其bType位值為3，bTag值為F



| bDataSize    | 0：0個位元組   1：1個位元組.   2：2個位元組.   3：4個位元組 |
| ------------ | ----------------------------------------------------------- |
| bLongItemTag | 0：main.  1：global.  2：local.  3：保留                    |
| data         | 資料                                                        |

物理描述符用來描述行為特性，是可選的。

**USB HID類可採用的通訊管道**

所有的HID裝置通過USB的控