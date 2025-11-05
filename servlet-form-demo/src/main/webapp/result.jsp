<%@ page contentType="text/html;charset=UTF-8" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>提交成功</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .icon {
            text-align: center;
            font-size: 50px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }
        td {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }
        td:first-child {
            font-weight: bold;
            color: #555;
            width: 120px;
        }
        .btn {
            display: block;
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">✅</div>
        <h1>提交成功！</h1>
        <table>
            <tr>
                <td>姓名</td>
                <td><%= request.getAttribute("name") %></td>
            </tr>
            <tr>
                <td>年龄</td>
                <td><%= request.getAttribute("age") %> 岁</td>
            </tr>
            <tr>
                <td>邮箱</td>
                <td><%= request.getAttribute("email") %></td>
            </tr>
            <tr>
                <td>手机号</td>
                <td><%= request.getAttribute("phone") != null && !request.getAttribute("phone").toString().isEmpty()
                    ? request.getAttribute("phone") : "未填写" %></td>
            </tr>
            <tr>
                <td>性别</td>
                <td><%= request.getAttribute("gender") != null && !request.getAttribute("gender").toString().isEmpty()
                    ? request.getAttribute("gender") : "未选择" %></td>
            </tr>
            <tr>
                <td>地址</td>
                <td><%= request.getAttribute("address") != null && !request.getAttribute("address").toString().isEmpty()
                    ? request.getAttribute("address") : "未填写" %></td>
            </tr>
        </table>
        <a href="index.html" class="btn">返回表单</a>
    </div>
</body>
</html>
