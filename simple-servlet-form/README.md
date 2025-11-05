# 超简单Servlet表单项目

一个最基础的Servlet表单提交示例，适合初学者学习。

## 🎯 项目功能

1. **表单输入** - 漂亮的HTML表单页面
2. **数据提取** - Servlet获取表单参数
3. **控制台打印** - 在Tomcat日志中打印数据
4. **结果显示** - JSP页面展示提交的数据

## 📁 项目结构

```
simple-servlet-form/
├── src/
│   └── main/
│       ├── java/
│       │   └── com/example/
│       │       └── FormServlet.java     # 表单处理Servlet
│       └── webapp/
│           ├── WEB-INF/
│           │   └── web.xml              # Web配置
│           ├── index.html               # 表单页面
│           └── result.jsp               # 结果页面
├── pom.xml                              # Maven配置
└── README.md
```

## 🚀 快速开始

### 方法一：在IDEA中运行

1. **用IDEA打开项目**
   - File → Open → 选择 `simple-servlet-form` 文件夹

2. **等待Maven下载依赖**

3. **配置Tomcat**
   - Run → Edit Configurations
   - 点击 `+` → Tomcat Server → Local
   - 配置Tomcat路径
   - Deployment → 添加 `simple-servlet-form:war exploded`
   - Application context 设为 `/`

4. **运行项目**
   - 点击运行按钮 ▶️

5. **访问应用**
   ```
   http://localhost:8080
   ```

### 方法二：命令行运行

```bash
# 1. 编译打包
mvn clean package

# 2. 部署WAR文件到Tomcat
cp target/simple-servlet-form.war $TOMCAT_HOME/webapps/

# 3. 启动Tomcat
$TOMCAT_HOME/bin/startup.sh

# 4. 访问
http://localhost:8080/simple-servlet-form
```

## 💡 使用流程

1. **打开首页**
   ```
   http://localhost:8080
   ```

2. **填写表单**
   - 姓名（必填）
   - 年龄（必填）
   - 邮箱（必填）
   - 手机号（选填）
   - 性别（选填）
   - 地址（选填）

3. **点击提交**

4. **查看结果**
   - 网页显示提交的数据
   - Tomcat控制台打印数据

## 📝 核心代码说明

### 1. 表单页面 (index.html)

```html
<form action="submitForm" method="post">
    <input type="text" name="name" required>
    <input type="number" name="age" required>
    <input type="email" name="email" required>
    <button type="submit">提交表单</button>
</form>
```

### 2. Servlet处理 (FormServlet.java)

```java
@WebServlet("/submitForm")
public class FormServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) {
        // 获取参数
        String name = request.getParameter("name");
        String age = request.getParameter("age");

        // 打印到控制台
        System.out.println("姓名: " + name);
        System.out.println("年龄: " + age);

        // 存储到request作用域
        request.setAttribute("name", name);
        request.setAttribute("age", age);

        // 转发到结果页面
        request.getRequestDispatcher("/result.jsp").forward(request, response);
    }
}
```

### 3. 结果页面 (result.jsp)

```jsp
<h1>提交成功！</h1>
<table>
    <tr>
        <td>姓名</td>
        <td><%= request.getAttribute("name") %></td>
    </tr>
    <tr>
        <td>年龄</td>
        <td><%= request.getAttribute("age") %></td>
    </tr>
</table>
```

## 🔧 技术栈

- **Java**: 17
- **Servlet**: Jakarta Servlet 6.0
- **JSP**: Jakarta JSP 3.1
- **构建工具**: Maven
- **服务器**: Tomcat 10.x

## 📖 学习要点

### 1. Servlet注解
```java
@WebServlet("/submitForm")  // 映射URL
```

### 2. 获取表单参数
```java
request.getParameter("name")  // 获取单个参数
```

### 3. 数据传递
```java
request.setAttribute("key", value)  // 设置属性
request.getAttribute("key")         // 获取属性
```

### 4. 页面跳转
```java
request.getRequestDispatcher("/result.jsp").forward(request, response);  // 转发
response.sendRedirect("index.html");  // 重定向
```

## 🎨 界面预览

### 表单页面
- 渐变背景
- 卡片式设计
- 响应式布局
- 输入验证

### 结果页面
- 成功图标
- 表格展示数据
- 返回按钮
- 打印功能

## ⚙️ 配置说明

### pom.xml
```xml
<dependencies>
    <!-- Servlet API -->
    <dependency>
        <groupId>jakarta.servlet</groupId>
        <artifactId>jakarta.servlet-api</artifactId>
        <version>6.0.0</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

### web.xml
```xml
<welcome-file-list>
    <welcome-file>index.html</welcome-file>
</welcome-file-list>
```

## 🐛 常见问题

### 1. 中文乱码
```java
request.setCharacterEncoding("UTF-8");
response.setCharacterEncoding("UTF-8");
```

### 2. 404错误
- 检查URL映射：`@WebServlet("/submitForm")`
- 检查表单action：`<form action="submitForm">`

### 3. 控制台看不到打印
- 查看Tomcat的catalina.out日志
- IDEA的Run窗口

## 📚 扩展建议

学完这个项目后，可以尝试：

1. ✅ 添加数据验证
2. ✅ 连接数据库保存数据
3. ✅ 添加文件上传功能
4. ✅ 使用Session保存用户信息
5. ✅ 添加AJAX异步提交

## 📄 许可证

本项目仅用于学习目的。

## 👨‍💻 适合人群

- Java Web初学者
- Servlet入门学习者
- 需要快速理解表单处理流程的开发者

---

**🎉 开始学习吧！**
