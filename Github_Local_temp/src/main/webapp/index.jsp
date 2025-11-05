<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.time.LocalDateTime" %>
<%@ page import="java.time.format.DateTimeFormatter" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maven + Tomcat Web 应用</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-align: center;
        }

        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 1.1em;
        }

        .info-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }

        .info-item:last-child {
            border-bottom: none;
        }

        .info-label {
            font-weight: bold;
            color: #555;
        }

        .info-value {
            color: #777;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .feature-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s;
        }

        .feature-card:hover {
            transform: translateY(-5px);
        }

        .feature-card h3 {
            margin-bottom: 10px;
            font-size: 1.2em;
        }

        .feature-card p {
            font-size: 0.9em;
            opacity: 0.9;
        }

        .links {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        }

        .btn {
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s;
            font-weight: bold;
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Maven + Tomcat Web 应用</h1>
        <p class="subtitle">基于Maven构建的企业级Web应用示例</p>

        <div class="info-section">
            <div class="info-item">
                <span class="info-label">当前时间：</span>
                <span class="info-value">
                    <%= LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")) %>
                </span>
            </div>
            <div class="info-item">
                <span class="info-label">服务器信息：</span>
                <span class="info-value"><%= application.getServerInfo() %></span>
            </div>
            <div class="info-item">
                <span class="info-label">Servlet版本：</span>
                <span class="info-value"><%= application.getMajorVersion() %>.<%= application.getMinorVersion() %></span>
            </div>
            <div class="info-item">
                <span class="info-label">会话ID：</span>
                <span class="info-value"><%= session.getId() %></span>
            </div>
        </div>

        <div class="features">
            <div class="feature-card">
                <h3>📦 Maven管理</h3>
                <p>使用Maven进行依赖管理和项目构建</p>
            </div>
            <div class="feature-card">
                <h3>🌐 Servlet支持</h3>
                <p>Jakarta Servlet 6.0 API</p>
            </div>
            <div class="feature-card">
                <h3>🎨 JSP页面</h3>
                <p>动态网页生成技术</p>
            </div>
            <div class="feature-card">
                <h3>🔧 RESTful API</h3>
                <p>支持RESTful风格接口</p>
            </div>
        </div>

        <div class="links">
            <a href="hello" class="btn">Hello Servlet</a>
            <a href="hello?name=张三" class="btn">带参数测试</a>
            <a href="user/list" class="btn btn-secondary">用户列表API</a>
            <a href="user-list.jsp" class="btn">用户管理页面</a>
        </div>

        <div class="footer">
            <p>Powered by Maven + Tomcat + IntelliJ IDEA 2025</p>
            <p>© 2025 示例Web应用程序</p>
        </div>
    </div>
</body>
</html>
