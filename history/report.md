## 操作系统实验1：可变分区存储管理

### 实验题目

编写一个C语言程序，模拟UNIX的可变分区内存管理，使用**循环首次适应法**实现对一块内存区域的分配和释放管理 。

### 实验目的

1. 加深对可变分区存储管理的理解。
2. 考察使用C语言编写代码的能力，特别是C语言编程的难点之一：指针的使用。
3. 复习使用指针实现链表以及在链表上的基本操作。  

### 算法思想

#### 可变分区存储

很容易从书本上了解到，可变分区存储管理并不预先将内存划分成分区，而是等到作业运行需要内存时就向系统申请，从空闲的内存区中申请占用空间，其大小等于作业所需内存大小。因此，可变分区存储不会产生“内零头”。每一个空闲分区使用一个map结构来进行管理，每个空闲分区按起始地址由低到高顺次登记在空闲分区存储表中。

#### 循环首次适应法

可变分区存储有多种管理方法：首次适应法、循环首次适应法、最佳适应法、最坏适应法，本次可变分区存储实现所采用的的算法思想就是循环首次适应法。

原理：把空闲表设计为顺序结构或双向链接结构的循环队列，各空闲区仍按地址从低到高的次序登记在空闲区的管理队列中。同时需设置起始查找指针，指向循环队列中的一个空闲区表项。

分配方式：总是从起始查找指针所指的表项开始查找。第一次找到满足要求的空闲区时，就分配所需大小的空闲区，修改表项，并调整起始查找指针，使其指向队列中被分配的后面的那块空闲区。下次分配时就从新指向的那块空闲区开始查找。

释放算法：释放时，如果被释放的区域不与空闲分区相邻，此时需要新增一块内存空间存储此释放区域，并将其加入空闲分区存储表中。如果被释放的区域与空闲分区相邻，则直接修改该空闲分区起始地址以及空间大小。

值得注意的是：非首次释放时，释放区与原空闲区相邻情况可归纳为四种情况（如图所示）![image-20210416201214963](assets/image-20210416201214963.png)

但也要考虑首次释放以及只有一个空闲区的情况。

### 算法实现

#### 数据结构&变量说明

##### 空闲块结构体

参考助教的实验指导文件，定义一个存储空闲块的结构体，用于构成双向循环列表，包含空闲块的大小、起始地址、前向指针、后向指针。

```c
typedef struct map{
    unsigned long m_size;
    char *m_addr;
    struct map *next, *prior;
} memFree;
```

##### 存储管理器结构体

自定义的用于管理可变分区的结构体，用于存储当前可变分区的信息，包含：目前的起始指针、整个可管理的内存空间的起始地址（不变）、剩余可分配空间、整个可管理的内存空间的大小（不变）、空闲块的数量。

```c
typedef struct map_mem_manage{
    memFree *mem_now;
    char *m_start_addr;
    unsigned long m_rest;
    unsigned long m_size;
    unsigned long m_free_count;
} memManage;
```

##### 基本变量说明（有规律）

- tmp_*：临时变量；
- mem_*：与结构体数据有关；
- m_*：结构体内部数据；
- ptr：在各个函数里都是用于替代起始指针进行操作的指针变量；
- pre：可作为临时变量；

#### 模块设计&接口说明

##### 接口定义

如下图，依次是：内存管理器初始化、分配函数、释放函数、打印空闲分区函数、打印错误函数（对算法无影响）、打印具体空闲块函数、打印声明（对算法无影响）。

```c
void initMemManage(memManage* mem_manager,unsigned long size,char *addr);
void lmalloc(memManage* mem_manager, unsigned long size);
void lfree(memManage* mem_manager, unsigned long size, char *addr);
void printFree(memManage* mem_manager);
void printError(char *str);
void printMemFree(memManage* mem_manager, memFree *mem_free);
void printDeclaration();
```

##### 模块设计

- 初始化模块

  1. 申请内存空间与内存管理器结构体空间
  2. 为内存管理器结构体初始化

  ```c
  /**
   * @brief initMemManage 初始化内存管理器
   * @param mem_manager 传入内存管理器
   * @param size 内存管理器的大小
   * @param addr 初始地址
   */
  void initMemManage(memManage* mem_manager,unsigned long size,char *addr){
      memFree *mem_free = (memFree*)malloc(sizeof (memFree));
      mem_free->m_addr = addr;
      mem_free->m_size=size;
      mem_free->next = mem_free;
      mem_free->prior = mem_free;
      mem_manager->mem_now = mem_free;
      mem_manager->m_start_addr = addr;
      mem_manager->m_rest = size;
      mem_manager->m_size = size;
      mem_manager->m_free_count = 1;
  }
  ```

- 分配内存模块

  主要思路：

  1. 判断所分配内存是否大于剩余可分配内存，如果大于，over；
  2. 从当前内存管理器储存的起始指针开始循环，在这里要注意中断点，因为这是个循环链表；
  3. 如果待分配内存小于当前空闲块，更改该空闲块起始地址即可，同时对内存管理器中的值做一些修改；
  4. 如果恰好等于当前空闲块，把当前空闲块剔除链表即可，同时对内存管理器中的值做一些修改；
  5. 如果找了一圈也没找着，打印error；

  代码展示：

  ```c
  /**
   * @brief lmalloc 分配内存
   * @param mem_manager
   * @param size
   */
  void lmalloc(memManage* mem_manager, unsigned long size){
      if(size>mem_manager->m_rest){
          printError("======no more free size!!=========");
          return;
      }
      int count = 1;
      memFree *ptr = mem_manager->mem_now;
      char *tmp_addr = ptr->m_addr;
      while(ptr){
          if(ptr->m_addr == tmp_addr) {
              if((count--)==0) {
                  printError("error:can not find fitable field;");
                  break;
              }
          }
          //如果待分配内存小于当前空闲块，更改该空闲块起始地址即可，同时对内存管理器中的值做一些修改；
          if(size<(ptr->m_size)){
             ptr->m_addr +=size;
             ptr->m_size -=size;
             mem_manager->m_rest-=size;
             mem_manager->mem_now = ptr;
             //printFree(mem_manager);
             break;
          }
          //如果恰好等于当前空闲块，把当前空闲块剔除链表即可，同时对内存管理器中的值做一些修改；
          else if (size==(ptr->m_size)) {
              memFree *tmp = ptr;
              mem_manager->mem_now=ptr->next;
              tmp->prior->next = tmp->next;
              tmp->next->prior = tmp->prior;
              free(tmp);
              mem_manager->m_rest-=size;
              mem_manager->m_free_count -=1;
              break;
          }
          else{
              ptr=ptr->next;
          }
      }
  }
  ```

  

- 释放内存模块

  主要思路：

  1. 先进行大体上的判别，比如释放地址低于起始地址等等；
  2. 判断是否还有空闲区，如果已经全部被分配，则新建一个空闲块；
  3. 如果待释放地址小于当前起始地址，那就把指针往左移动，直到当前指针刚好大于待释放起始指针或者已经到达了最左边的空闲区了；
  4. 找到这个空闲区后再次进行判断，如果待释放的区域与空闲区域进行了重叠，报错处理；如果与右边邻近，那就把空闲块的起始地址改一改，如果既与右边邻近，由于左边邻近，那就合并处理；做这些操作的同时，也要修改内存管理器中的一些值；
  5. 如果待释放区域大于当前起始指针，与3相似的处理，不予赘述；
6. 如果等于当前起始指针，直接报错；

  代码展示：由于代码挺长的，仅展示在空闲块左边的一种情况，全部代码可见附录或者源代码。

  ```c
  /**
   * @brief lfree 释放内存模块
   * @param mem_manager 传入内存管理器
   * @param size 传入释放内存大小
   * @param addr 传入释放内存的起始地址
   */
  void lfree(memManage *mem_manager, unsigned long size, char *addr)
  {
      // 仅展示一种情况，全部代码可见附录或者源代码
      // 如果空间已经全部被分配，则需要新建列表，用于创建链表
      if(mem_manager->m_rest==0){
          memFree *mem_free = (memFree *)malloc(sizeof(memFree));
          mem_free->m_addr = addr;
          mem_free->m_size = size;
          mem_free->next = mem_free;
          mem_free->prior = mem_free;
          mem_manager->mem_now = mem_free;
          mem_manager->m_rest = size;
          mem_manager->m_free_count = 1;
          return;
      }
      memFree *ptr = mem_manager->mem_now;
      memFree *pre;
      memFree *m_next;
      if (addr < ptr->m_addr)
      {
          while (ptr->prior->m_addr >= addr && (ptr->prior->m_addr) < ptr->m_addr)
          {
              ptr = ptr->prior;
          }
          if (ptr->m_addr == addr)
          {
              printError("error: addr overlay");
              return;
          }
          if ((addr > ptr->prior->m_addr && addr < ptr->prior->m_addr + ptr->prior->m_size) || (addr + size) > ptr->m_addr)
          {
              printError("error:addr overlay");
              return;
          }
          else if (addr > ptr->prior->m_addr && addr == ptr->prior->m_addr + ptr->prior->m_size)
          {
              if ((addr + size) < ptr->m_addr)
              {
                  pre = ptr->prior;
                  pre->m_size += size;
                  mem_manager->m_rest += size;
              }
              else if ((addr + size) == ptr->m_addr)
              {
                  pre = ptr->prior;
                  pre->prior->next = ptr;
                  ptr->prior = pre->prior;
                  ptr->m_addr = pre->m_addr;
                  ptr->m_size = pre->m_size + size;
                  mem_manager->m_rest += size;
                  mem_manager->m_free_count -= 1;
                  free(pre);
              }
          }
          else if ((addr + size) == ptr->m_addr)
          {
              ptr->m_addr -= size;
              ptr->m_size += size;
              mem_manager->m_rest += size;
          }
          else
          {
              memFree *new_mem_free = (memFree *)malloc(sizeof(memFree));
              new_mem_free->m_addr = addr;
              new_mem_free->m_size = size;
              new_mem_free->next = ptr;
              new_mem_free->prior = ptr->prior;
              ptr->prior->next = new_mem_free;
              ptr->prior = new_mem_free;
              mem_manager->m_rest += size;
              mem_manager->m_free_count += 1;
              return;
          }
      }
      else
      {
          printError("error:addr overlay");
          return;
      }
  }
  ```

### 测试&效果

#### 测试输入格式

由于使用了重定向输入输出，所以只需要提前把数据输入到重定向输入文件中即可。

- `m size` 其中m指分配内存，size指分配内存大小；
- `f size addr` 其中f指释放内存，size指释放内存大小，addr为起始地址，这里是相对地址，其实最后还是转化为绝对地址做的，只不过这里方便测试；
- `e` 终止符号；

测试输入命令：`./os-lab1.exe < in_5ferror.txt > out5.txt`

```
m 100 
f 60 0
e
```

#### 各种效果

输出解释：

1. 每一条命令的所有输出均在两条\==\==\==\==\==\===之间；
2. 输出command命令，以及命令信息；
3. 打印在分配或者释放过程中出现的错误；
4. 打印分配或者释放之后的结果，以start print未开始，以finish print为结束；
5. 在start print开始的时候，先打印剩余内存基本信息，比如个数以及内存量等等；

具体样例展示：

- 要求分配内存过大

  程序输入：

  ```
  m 1001
  e
  ```

  程序输出结果：

  ```txt
  =============================================
  command:malloc,size:1001
  error:======no more free size!!=========
  ================the rest mem :===============
  ==============start  print!!=================
  ==============number of free:1===============
  ============all size of free:1000=============
  =============================================
  addr:0
  size:1000
  =============================================
  ==============finish print!!=================
  =============================================
  
  exit
  ```

- 体现循环首次适应法

  程序输入：

  先制作几个不相连的空闲块，然后分配一个内存，观察分配结果；

  ```
  m 900
  f 100 0
  f 100 150
  f 200 300
  m 150
  e
  ```

  程序输出：

  此段截取后面的两个命令之后的结果输出，完整版请移至源码目录观看；

  ```
  =============================================
  command:lfree,addr:1774460,size:200
  ================the rest mem :===============
  ==============start  print!!=================
  ==============number of free:4===============
  ============all size of free:500=============
  =============================================
  addr:900
  size:100
  =============================================
  =============================================
  addr:0
  size:100
  =============================================
  =============================================
  addr:150
  size:100
  =============================================
  =============================================
  addr:300
  size:200
  =============================================
  ==============finish print!!=================
  =============================================
  
  =============================================
  command:malloc,size:150
  ================the rest mem :===============
  ==============start  print!!=================
  ==============number of free:4===============
  ============all size of free:350=============
  =============================================
  addr:450
  size:50
  =============================================
  =============================================
  addr:900
  size:100
  =============================================
  =============================================
  addr:0
  size:100
  =============================================
  =============================================
  addr:150
  size:100
  =============================================
  ==============finish print!!=================
  =============================================
  ```

- 释放已经存满的情况

  程序输入

  ```
  m 1000
  f 100 1
  e
  ```

  程序输出

  可以明显看到打印出了我们想要的情况；

  ```
  =============================================
  command:malloc,size:1000
  ================the rest mem :===============
  ===============start  print!!================
  ==============no free print!!================
  ==============finish print!!=================
  =============================================
  
  =============================================
  command:lfree,addr:10228305,size:100
  ================the rest mem :===============
  ==============start  print!!=================
  ==============number of free:1===============
  ============all size of free:100=============
  =============================================
  addr:1
  size:100
  =============================================
  ==============finish print!!=================
  =============================================
  
  exit
  ```

-  释放内存与右边临近（参照in_3fsm.txt和out3.txt）这里不再过多展示，可参考文件夹中的输出文件观看；

- 释放内存与左边临近（参照in_4fbig.txt和out4.txt）这里不再过多展示；

- 释放内存错误（参照in_5ferroe.txt和out5.txt）不再展示；

另外还制作了一个比较长的样例，也放在了源码目录下in.txt；

### 错误输出

在这里列举一些会引发报错的情况

- 分配内存空间不够：error:=\==\==\=no more free size!!=\====\=\==\=";
- 找了一圈没找到合适的：error:can not find fitable field;
- 释放内存，与空闲区重叠：error:addr overlay；
- 释放内存过大等等；

### 总结&收获

在这次实验中，我加深对可变分区存储管理的理解，使用了双向指针完成循环列表指针的使用，巩固了指针在链表上的基本操作。此外，我还学到了重定向输入输出等一些实用的小技巧。  

此外，在这次项目中我首次使用了qtcreator来作为我的IDE，觉得这款编译器具有占用内存小，启动快等优点，是一次不错的尝试；

程序中的关键点主要是释放，释放中需要考虑首次释放和非首次释放，这里我使用了大量的逻辑判断语句来实现这一功能，另外实验需要考虑不同程度的报错处理，所以我实现了报错接口，使用方便；

内存申请过之后，最后要进行释放。

实验的总体难度不大，在规定时间内可以顺利完成，感谢刘老师的指导和帮助！！

### 附录

#### 代码附录

```c
#include <stdio.h>
#include <stdlib.h>
#define MAX_SIZE 1000
typedef struct map
{
    unsigned long m_size;
    char *m_addr;
    struct map *next, *prior;
} memFree;
typedef struct map_mem_manage
{
    memFree *mem_now;
    char *m_start_addr;
    unsigned long m_rest;
    unsigned long m_size;
    unsigned long m_free_count;
} memManage;
void initMemManage(memManage *mem_manager, unsigned long size, char *addr);
void lmalloc(memManage *mem_manager, unsigned long size);
void lfree(memManage *mem_manager, unsigned long size, char *addr);
void printFree(memManage *mem_manager);
void printError(char *str);
void printMemFree(memManage *mem_manager, memFree *mem_free);
void printDeclaration();
int main()
{
    // create memmanager and malloc 1000 for operation
    memManage *mem_manager = (memManage *)malloc(sizeof(memManage));
    char *mem_addr = (char *)malloc(MAX_SIZE * sizeof(int));
    char *tmp_addr;
    //freopen("in.txt", "r", stdin);
    //freopen("out.txt", "w", stdout);
    initMemManage(mem_manager, MAX_SIZE, mem_addr);
    char command_char;
    unsigned long size;
    unsigned long addr;
    while (scanf("%c", &command_char))
    {
        if (command_char == 'm')
        {
            scanf("%lu", &size);
            printf("=============================================\n");
            printf("command:%calloc,size:%lu\n", command_char, size);
            lmalloc(mem_manager, size);
            printf("================the rest mem :===============\n");
            printFree(mem_manager);
            printf("=============================================\n\n");
            getchar();
            //printf("command_char:%csize:%lu\n",command_char,size);
        }
        if (command_char == 'f')
        {
            scanf("%lu %lu", &size, &addr);
            getchar();
            tmp_addr = mem_addr + addr;
            printf("=============================================\n");
            printf("command:l%cree,addr:%lu,size:%lu\n", command_char, mem_addr + addr, size);
            lfree(mem_manager, size, tmp_addr);
            printf("================the rest mem :===============\n");
            printFree(mem_manager);
            printf("=============================================\n\n");
        }
        if (command_char == 'e')
        {
            printf("exit\n");
            break;
        }
    }
    printDeclaration();
    memFree *tmp;
    memFree *ptr = mem_manager->mem_now;
    for(int i=0;i<(mem_manager->m_free_count-1);++i){
        tmp = ptr->next;
        free(ptr);
        ptr=tmp;
    }
    free(ptr);
    free(mem_manager);
    fclose(stdin);
    fclose(stdout);
    return 0;
}
/**
 * @brief initMemManage 初始化内存管理器
 * @param mem_manager 传入内存管理器
 * @param size 内存管理器的大小
 * @param addr 初始地址
 */
void initMemManage(memManage *mem_manager, unsigned long size, char *addr)
{
    memFree *mem_free = (memFree *)malloc(sizeof(memFree));
    mem_free->m_addr = addr;
    mem_free->m_size = size;
    mem_free->next = mem_free;
    mem_free->prior = mem_free;
    mem_manager->mem_now = mem_free;
    mem_manager->m_start_addr = addr;
    mem_manager->m_rest = size;
    mem_manager->m_size = size;
    mem_manager->m_free_count = 1;
}
/**
 * @brief lmalloc 分配内存
 * @param mem_manager
 * @param size
 */
void lmalloc(memManage *mem_manager, unsigned long size)
{
    if (size > mem_manager->m_rest)
    {
        printError("======no more free size!!=========");
        return;
    }
    int count = 1;
    memFree *ptr = mem_manager->mem_now;
    char *tmp_addr = ptr->m_addr;
    while (ptr)
    {
        if (ptr->m_addr == tmp_addr)
        {
            if ((count--) == 0)
            {
                printError("can not find fitable field;");
                break;
            }
        }
        //如果待分配内存小于当前空闲块，更改该空闲块起始地址即可，同时对内存管理器中的值做一些修改；
        if (size < (ptr->m_size))
        {
            ptr->m_addr += size;
            ptr->m_size -= size;
            mem_manager->m_rest -= size;
            mem_manager->mem_now = ptr;
            //printFree(mem_manager);
            break;
        }
        //如果恰好等于当前空闲块，把当前空闲块剔除链表即可，同时对内存管理器中的值做一些修改；
        else if (size == (ptr->m_size))
        {
            memFree *tmp = ptr;
            mem_manager->mem_now = ptr->next;
            tmp->prior->next = tmp->next;
            tmp->next->prior = tmp->prior;
            free(tmp);
            mem_manager->m_rest -= size;
            mem_manager->m_free_count -= 1;
            break;
        }
        else
        {
            ptr = ptr->next;
        }
    }
}
/**
 * @brief lfree 释放内存模块
 * @param mem_manager 传入内存管理器
 * @param size 传入释放内存大小
 * @param addr 传入释放内存的起始地址
 */
void lfree(memManage *mem_manager, unsigned long size, char *addr)
{
    if (size == 0)
    {
        printError("no size;");
        return;
    }
    if (addr < mem_manager->m_start_addr)
    {
        printError("too low;");
        return;
    }
    if (addr > mem_manager->m_start_addr + mem_manager->m_size)
    {
        printError(" too high;");
        return;
    }
    if ((addr + size) > (mem_manager->m_start_addr + mem_manager->m_size))
    {
        printError("too high;");
        return;
    }
    if(mem_manager->m_rest==0){
        memFree *mem_free = (memFree *)malloc(sizeof(memFree));
        mem_free->m_addr = addr;
        mem_free->m_size = size;
        mem_free->next = mem_free;
        mem_free->prior = mem_free;
        mem_manager->mem_now = mem_free;
        mem_manager->m_rest = size;
        mem_manager->m_free_count = 1;
        return;
    }
    memFree *ptr = mem_manager->mem_now;
    memFree *pre;
    memFree *m_next;
    if (addr < ptr->m_addr)
    {
        while (ptr->prior->m_addr >= addr && (ptr->prior->m_addr) < ptr->m_addr)
        {
            ptr = ptr->prior;
        }
        if (ptr->m_addr == addr)
        {
            printError("error: addr overlay");
            return;
        }
        if ((addr > ptr->prior->m_addr && addr < ptr->prior->m_addr + ptr->prior->m_size) || (addr + size) > ptr->m_addr)
        {
            printError("error:addr overlay");
            return;
        }
        else if (addr > ptr->prior->m_addr && addr == ptr->prior->m_addr + ptr->prior->m_size)
        {
            if ((addr + size) < ptr->m_addr)
            {
                pre = ptr->prior;
                pre->m_size += size;
                mem_manager->m_rest += size;
            }
            else if ((addr + size) == ptr->m_addr)
            {
                pre = ptr->prior;
                pre->prior->next = ptr;
                ptr->prior = pre->prior;
                ptr->m_addr = pre->m_addr;
                ptr->m_size = pre->m_size + size;
                mem_manager->m_rest += size;
                mem_manager->m_free_count -= 1;
                free(pre);
            }
        }
        else if ((addr + size) == ptr->m_addr)
        {
            ptr->m_addr -= size;
            ptr->m_size += size;
            mem_manager->m_rest += size;
        }
        else
        {
            memFree *new_mem_free = (memFree *)malloc(sizeof(memFree));
            new_mem_free->m_addr = addr;
            new_mem_free->m_size = size;
            new_mem_free->next = ptr;
            new_mem_free->prior = ptr->prior;
            ptr->prior->next = new_mem_free;
            ptr->prior = new_mem_free;
            mem_manager->m_rest += size;
            mem_manager->m_free_count += 1;
            return;
        }
    }
    else if (addr > ptr->m_addr)
    {
        while (ptr->next->m_addr <= addr && (ptr->next->m_addr) > ptr->m_addr)
        {
            ptr = ptr->next;
        }
        if (ptr->m_addr == addr)
        {
            printError("error: addr overlay");
            return;
        }
        if ((addr < ptr->next->m_addr && (addr + size) > ptr->next->m_addr) || (addr) < (ptr->m_addr + ptr->m_size))
        {
            printError("error:addr overlay");
            return;
        }
        else if (addr < ptr->next->m_addr && (addr + size) == ptr->next->m_addr)
        {
            if (addr > (ptr->m_addr + ptr->m_size))
            {
                pre = ptr->next;
                pre->m_addr -= size;
                pre->m_size += size;
                mem_manager->m_rest += size;
            }
            else if (addr == (ptr->m_addr + ptr->m_size))
            {
                pre = ptr->next;
                pre->next->prior = ptr;
                ptr->next = pre->next;
                ptr->m_size = pre->m_size + size;
                mem_manager->m_rest += size;
                mem_manager->m_free_count -= 1;
                free(pre);
            }
        }
        else if (addr == (ptr->m_addr + ptr->m_size))
        {
            ptr->m_size += size;
            mem_manager->m_rest += size;
        }
        else
        {
            memFree *new_mem_free = (memFree *)malloc(sizeof(memFree));
            new_mem_free->m_addr = addr;
            new_mem_free->m_size = size;
            new_mem_free->prior = ptr;
            new_mem_free->next = ptr->next;
            ptr->next->prior = new_mem_free;
            ptr->next = new_mem_free;
            mem_manager->m_rest += size;
            mem_manager->m_free_count += 1;
            return;
        }
    }
    else
    {
        printError("error:addr overlay");
        return;
    }
}
void printFree(memManage *mem_manager)
{
    if (mem_manager->m_rest == 0)
    {
        printf("===============start  print!!================\n");

        printf("==============no free print!!================\n");
        printf("==============finish print!!=================\n");
        return;
    }
    memFree *ptr = mem_manager->mem_now;
    char *flag_addr = ptr->m_addr;
    int count = 1;
    printf("==============start  print!!=================\n");

    printf("==============number of free:%lu===============\n", mem_manager->m_free_count);
    printf("============all size of free:%lu=============\n", mem_manager->m_rest);
    while (1)
    {
        if (ptr->m_addr == flag_addr)
        {
            if ((count--) == 0)
            {
                printf("==============finish print!!=================\n");
                break;
            }
        }
        printMemFree(mem_manager, ptr);
        ptr = ptr->next;
    }
}
void printError(char *str)
{
    printf("error:%s\n", str);
}

void printMemFree(memManage *mem_manager, memFree *mem_free)
{
    printf("=============================================\n");
    printf("addr:%lu\nsize:%lu\n", mem_free->m_addr - mem_manager->m_start_addr, mem_free->m_size);
    printf("=============================================\n");
}

void printDeclaration()
{
    printf("=============================================\n");
    printf("===============end     program!!===============\n");
    printf("===========518030910019 tongzhixin===========\n");
    printf("=============================================\n");
}

```

#### 程序输入附录

![image-20210418132805993](assets/image-20210418132805993.png)

#### 程序输出附录

![image-20210418132823182](assets/image-20210418132823182.png)