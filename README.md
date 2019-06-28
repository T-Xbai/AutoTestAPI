#### 前言：此项目纯属个人学习编写，如有不好的地方，意见，吐槽给小白我指出。🙏

#### 介绍：这个项目主要还是实现用 Excel 和 Json 文件结合做的一个数据驱动，实现接口自动化。







### 操作说明：

##### 

##### 一、Excel 模版：

**说明：**

​    ⚠️  Excel 文件必须存放在`app -> test_data ->case_data`目录下

​    ⚠️  Excel 内每一行代表一条测试 case ，列名顺序不固定，但是模版内的固定列名必须存在。

| 用例编号 | 测试目的     | 测试接口                | 请求方法 | 请求数据            | 是否执行 | 是否通过 |
| -------- | ------------ | ----------------------- | -------- | ------------------- | -------- | -------- |
| login_01 | 用户有效登录 | /member/butler_login.do | POST     | login/test_login_01 | N        |          |

- **用例编号：** 用例编号在同一个 Excel 工作簿中是不可重复的

- **测试目的：** 用于描述此条 case 执行的目的

- **测试接口：** 测试接口的地址

- **请求方法：** `GET`，`POST`，`PUT`, `DELETE` 等

- **请求数据：** 此处填写的是该条 case 对应的 json 文件的地址。系统默认读取的是项目的 `AutoTestAPI -> app -> test_data ->json_data` 目录下的 json 文件。

  例如： `json_data -> login -> test_login_01.json` 只需要填写 `login/test_login_01`即可
  
  ![image.png](https://upload-images.jianshu.io/upload_images/6213878-372c26270ac8d813.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




- **是否执行：** `Y` 代表执行，`N`代表不执行

- **是否通过：** TODO 因为项目有报告输出，就没有去实现了



##### 二、Json 文件模版：

⚠️  所有介绍字段可以为 `null` 但是都必须存在。

⚠️  变量使用的统一格式为：`{{ 变量名 }}`

**1. 字段介绍：**

- **url :** 请求接口的 `URL` 链接，`URL` 的`host` 可以使用 `{{ url }}`变量进行替换

  说明：`{{ url }}`的值可以在 `conf -> conf.yaml`文件内进行配置，方便环境切换

- **method :**  请求方法

- **headers : ** 请求头设置

  样例：

  ```json
  "headers": {
    "content-type": "application/json"
  },
  ```

- **rely_cases : ** 依赖 `case` 设置，用于前置条件的执行，可以将前置条件的响应数据，作为变量使用

  ⚠️  `rely_cases` 是一个` list`

  **字段介绍 ：**

  - **case_id :**  填写的是依赖 Case 的用例编号

    格式:`工作簿名称.用例编号` ,存在分隔符`.`

    例如: `Login.login_01`

  - **fields :** 依赖 case 的字段，字段的值填写的是匹配表达式，支持：`jsonpath` 和 `正则表达式`

    样例：

    ```json
    "rely_cases": [
      {
        "case_id": "Login.login_01",
        "fields": {
          "username": "$.username",
          "password": "$.password"
        }
      },
      {
        "case_name": "login_02",
        "fields": null
      }
    ]
    ```

    字段要在数据中使用，直接 `{{ 字段名 }}`即可，系统会替换匹配的数据

    

- **body :** 请求数据

- **files :** 用于文件上传接口，不使用的时候可以值为 `null`

  样例：

  ```json
  "files": {
    "file1": "image_01.png",
    "file2": "上传文件的地址，文件必须存放在 test_data -> files 目录下"
  }
  ```

- **asserts :**  用于测试后断言

  ```json
  "asserts": {
    "code": 200, 											//	响应状态
    "$.username": "13681950786",      //  key 为 jsonpath 表达式，value 是需要断言的值
    "isContains": "hello"             //  代表的是响应数据当中是否包含 `hello` 这个值
  }
  
  -- 说明： 需要其它断言方式，或者断言其它数据，可以根据需求在方法内扩展
  ```

- **db_config :** 用于数据库连接配置，因为涉及到不同的 `case` 操作的数据库不同，所以可以在此处单独配置连接

  ⚠️ 项目现阶段只支持 `mysql` 连接

  ⚠️ 该字段是允许为  `null` 的，他会默认读取 `conf -> conf.yaml` 配置文件中的数据库配置

   **字段介绍**：

  ​	比较灵活的是，之后需要配置其它数据库的话，连接方式不一致，可以根据不同字段设置

  - **db_type :** 数据库类型

  - **username :**  用户名

  - **password :** 密码

  - **host :**  连接的域名

    

- **after :** 用于这条 case 执行结束后的善后工作，例如脏数据删除

  **字段介绍 ：**
  
  - **veriables :**  提取响应结果的字段值，并以变量的方式使用
  
    样例：
  
    ```
    "variables": {
      "user_id": "$.id",
      "user_name": "$.name",
      "user_key": "^h(*.?)o"
    }
    
    ```
  
  - **db_executes :** 执行`sql`语句
  
    样例：
  
    ```js
    "db_executes": [
      {
        "name": "data_base",   // 指定需要执行的数据库
        "sql": [  						 // 执行的 sql 集合
          "select * from User where name = {{ user_name }}", //变量的使用
          "select * from User where id = {{ user_id }}",
          "select * from User where key = {{ user_key }}"
        ]
      },
      {
        "name": "data_base",
        "sql": [
          "select * from User where name = {{ user_name }}",
          "select * from User where id = {{ user_id }}",
          "select * from User where key = {{ user_key }}"
        ]
      }
    ]
    ```





##### 三、执行 Case 

1. 进入项目的 `test` 目录下，执行命令：

   ```python
   pytest --alluredir=../report/allure_results
   ```

2. 或者直接在 `test_run.py` 直接执行

   

##### 四、报告展示

​	一般 case 执行完成以后，会在 `report/allure_results` 中生成报告数据

​    执行命令：

```python
>>> allure serve report/allure_results

Generating report to temp directory...
Report successfully generated to /var/folders/sy/bxf_1_yn06s7sm2yzm97r2b80000gn/T/7447734840827014947/allure-report
Starting web server...
2019-06-28 14:39:20.885:INFO::main: Logging initialized @2633ms to org.eclipse.jetty.util.log.StdErrLog
Server started at <http://127.0.0.1:55969/>. Press <Ctrl+C> to exit
```

运行后浏览器就会默认打开报告地址：

![image.png](https://upload-images.jianshu.io/upload_images/6213878-083594040b61bade.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



#### 五、 项目中有 flask 写的小接口，可以用来测试玩玩😂

| URL                                          | METHOD | description    |
| -------------------------------------------- | ------ | -------------- |
| http://localhost:5000/getUserPassword        | GET    | 获取用户名密码 |
| http://localhost:5000/member/butler_login.do | POST   | 模仿登陆接口   |
| http://localhost:5000/upload/image | POST |模仿上传接口|



###### 项目大体功能就这些啦，有不足和意见还有吐槽，都可以给小白我指出，进步就靠大佬们了🙏

------

