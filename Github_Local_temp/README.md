# Maven + Tomcat Web 应用程序

这是一个基于Maven构建的完整Java Web应用程序示例，适用于IntelliJ IDEA 2025和Apache Tomcat服务器。

## 项目特性

- ✅ Maven项目管理
- ✅ Jakarta Servlet 6.0 API
- ✅ JSP页面支持
- ✅ RESTful API示例
- ✅ 用户管理CRUD操作
- ✅ 字符编码过滤器
- ✅ 错误页面处理
- ✅ Logback日志管理
- ✅ 响应式UI设计

## 技术栈

- **构建工具**: Maven 3.x
- **JDK**: Java 17
- **应用服务器**: Apache Tomcat 10.x
- **Servlet**: Jakarta Servlet 6.0
- **JSP**: Jakarta JSP 3.1
- **JSTL**: Jakarta JSTL 3.0
- **JSON处理**: Gson 2.10.1
- **数据库**: MySQL (可选)
- **日志**: Logback 1.4.14
- **IDE**: IntelliJ IDEA 2025

## 项目结构

```
maven-tomcat-webapp/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── example/
│   │   │           ├── servlet/          # Servlet控制器
│   │   │           │   ├── HelloServlet.java
│   │   │           │   ├── UserServlet.java
│   │   │           │   └── CharacterEncodingFilter.java
│   │   │           ├── model/            # 数据模型
│   │   │           │   └── User.java
│   │   │           ├── service/          # 业务逻辑层
│   │   │           │   └── UserService.java
│   │   │           └── dao/              # 数据访问层
│   │   ├── resources/
│   │   │   └── logback.xml               # 日志配置
│   │   └── webapp/
│   │       ├── WEB-INF/
│   │       │   └── web.xml               # Web应用配置
│   │       ├── css/
│   │       │   └── style.css             # 样式文件
│   │       ├── js/                       # JavaScript文件
│   │       ├── images/                   # 图片资源
│   │       ├── error/                    # 错误页面
│   │       │   ├── 404.jsp
│   │       │   └── 500.jsp
│   │       ├── index.jsp                 # 首页
│   │       └── user-list.jsp             # 用户列表页面
│   └── test/
│       └── java/                         # 测试代码
├── .idea/                                # IntelliJ IDEA配置
│   ├── runConfigurations/
│   │   └── Tomcat.xml                    # Tomcat运行配置
│   ├── compiler.xml
│   └── misc.xml
├── pom.xml                               # Maven配置文件
├── .gitignore
└── README.md
```

## 快速开始

### 前置要求

1. **安装JDK 17**
   - 下载地址: https://www.oracle.com/java/technologies/downloads/
   - 配置JAVA_HOME环境变量

2. **安装Maven**
   - 下载地址: https://maven.apache.org/download.cgi
   - 配置Maven环境变量

3. **安装Apache Tomcat 10.x**
   - 下载地址: https://tomcat.apache.org/download-10.cgi
   - 解压到本地目录

4. **安装IntelliJ IDEA 2025**
   - 下载地址: https://www.jetbrains.com/idea/download/

### 使用IntelliJ IDEA运行

1. **打开项目**
   ```
   File -> Open -> 选择maven-tomcat-webapp目录
   ```

2. **配置Tomcat**
   ```
   Run -> Edit Configurations
   点击 '+' -> Tomcat Server -> Local
   配置Tomcat Home目录
   在Deployment标签页添加Artifact: maven-tomcat-webapp:war exploded
   Application context设置为: /
   ```

3. **运行项目**
   ```
   点击运行按钮或按Shift+F10
   ```

4. **访问应用**
   ```
   浏览器访问: http://localhost:8080
   ```

### 使用Maven命令运行

1. **编译项目**
   ```bash
   mvn clean compile
   ```

2. **打包WAR文件**
   ```bash
   mvn clean package
   ```

3. **部署到Tomcat**
   ```bash
   # 将target/maven-tomcat-webapp.war复制到Tomcat的webapps目录
   cp target/maven-tomcat-webapp.war $TOMCAT_HOME/webapps/

   # 启动Tomcat
   $TOMCAT_HOME/bin/startup.sh  # Linux/Mac
   $TOMCAT_HOME/bin/startup.bat # Windows
   ```

4. **使用Maven Tomcat插件运行**
   ```bash
   mvn tomcat7:run
   ```

## API接口

### 用户管理API (RESTful)

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/user/list` | 获取所有用户 |
| GET | `/user/{id}` | 获取指定用户 |
| POST | `/user/` | 创建新用户 |
| PUT | `/user/{id}` | 更新用户 |
| DELETE | `/user/{id}` | 删除用户 |

### API使用示例

**获取所有用户**
```bash
curl http://localhost:8080/user/list
```

**获取单个用户**
```bash
curl http://localhost:8080/user/1
```

**创建用户**
```bash
curl -X POST http://localhost:8080/user/ \
  -H "Content-Type: application/json" \
  -d '{"username":"测试用户","email":"test@example.com","password":"123456","age":25,"phone":"13800138000"}'
```

**更新用户**
```bash
curl -X PUT http://localhost:8080/user/1 \
  -H "Content-Type: application/json" \
  -d '{"username":"更新用户","email":"updated@example.com","age":26}'
```

**删除用户**
```bash
curl -X DELETE http://localhost:8080/user/1
```

## 页面路由

| 路径 | 描述 |
|------|------|
| `/` 或 `/index.jsp` | 应用首页 |
| `/hello` | Hello Servlet示例 |
| `/hello?name=张三` | 带参数的Servlet |
| `/user-list.jsp` | 用户管理页面 |
| `/error/404.jsp` | 404错误页面 |
| `/error/500.jsp` | 500错误页面 |

## 配置说明

### Maven配置 (pom.xml)

- **Java版本**: 17
- **Servlet API**: Jakarta Servlet 6.0
- **JSP API**: Jakarta JSP 3.1
- **编码**: UTF-8
- **打包方式**: WAR

### Web配置 (web.xml)

- **会话超时**: 30分钟
- **字符编码**: UTF-8
- **欢迎页面**: index.jsp
- **错误页面**: 404.jsp, 500.jsp

### 日志配置 (logback.xml)

- **日志级别**: INFO (根级别), DEBUG (应用级别)
- **输出方式**: 控制台 + 文件
- **日志文件**: logs/application.log
- **滚动策略**: 按天滚动，单文件最大10MB，保留30天

## 开发指南

### 添加新的Servlet

1. 在`src/main/java/com/example/servlet/`创建新的Servlet类
2. 继承`HttpServlet`并重写`doGet()`或`doPost()`方法
3. 在`web.xml`中配置Servlet映射
4. 或使用`@WebServlet`注解（需要Servlet 3.0+）

### 添加新的JSP页面

1. 在`src/main/webapp/`创建新的JSP文件
2. 使用JSTL标签库简化页面开发
3. 引用`css/style.css`保持统一样式

### 添加Maven依赖

在`pom.xml`的`<dependencies>`标签中添加新的依赖：
```xml
<dependency>
    <groupId>组织ID</groupId>
    <artifactId>构件ID</artifactId>
    <version>版本号</version>
</dependency>
```

## 常见问题

### 1. 端口被占用
修改Tomcat配置中的端口号（默认8080）

### 2. 字符编码问题
项目已配置CharacterEncodingFilter，确保所有文件使用UTF-8编码

### 3. 热部署不生效
在IDEA中确保配置了"On frame deactivation: Update classes and resources"

### 4. Maven依赖下载失败
检查网络连接或配置Maven镜像（如阿里云镜像）

## 项目扩展

可以在此基础上扩展以下功能：

- [ ] 集成Spring Framework
- [ ] 添加数据库持久化（MyBatis/JPA）
- [ ] 实现用户认证和授权
- [ ] 添加前端框架（Vue.js/React）
- [ ] 集成Redis缓存
- [ ] 添加单元测试和集成测试
- [ ] 实现文件上传下载
- [ ] 添加WebSocket支持
- [ ] 集成Swagger API文档

## 许可证

本项目仅用于学习和演示目的。

## 作者

Maven Tomcat Web Application Example

## 更新日志

### v1.0.0 (2025-11-05)
- ✅ 初始版本发布
- ✅ 基础Maven项目结构
- ✅ Servlet和JSP示例
- ✅ RESTful API实现
- ✅ 用户管理功能
- ✅ 错误页面处理
- ✅ 日志管理配置
- ✅ IDEA Tomcat配置

## 联系方式

如有问题或建议，欢迎提Issue或Pull Request。
