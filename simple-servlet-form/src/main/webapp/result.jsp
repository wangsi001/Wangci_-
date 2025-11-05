<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>提交成功</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }

        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 28px;
        }

        .success-icon {
            text-align: center;
            font-size: 60px;
            margin-bottom: 20px;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }

        .data-table tr {
            border-bottom: 1px solid #f0f0f0;
        }

        .data-table tr:last-child {
            border-bottom: none;
        }

        .data-table td {
            padding: 15px;
        }

        .data-table td:first-child {
            font-weight: bold;
            color: #555;
            width: 120px;
            background: #f8f9fa;
            border-right: 2px solid #e0e0e0;
        }

        .data-table td:last-child {
            color: #333;
        }

        .value {
            font-size: 16px;
        }

        .empty-value {
            color: #999;
            font-style: italic;
        }

        .btn-group {
            display: flex;
            gap: 15px;
            justify-content: center;
        }

        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }

        .btn-secondary:hover {
            background: #d0d0d0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="success-icon">✅</div>
        <h1>提交成功！</h1>
        <p class="subtitle">您提交的信息如下：</p>

        <table class="data-table">
            <tr>
                <td>姓名</td>
                <td class="value">
                    <%= request.getAttribute("name") != null ? request.getAttribute("name") : "<span class='empty-value'>未填写</span>" %>
                </td>
            </tr>
            <tr>
                <td>年龄</td>
                <td class="value">
                    <%= request.getAttribute("age") != null ? request.getAttribute("age") + " 岁" : "<span class='empty-value'>未填写</span>" %>
                </td>
            </tr>
            <tr>
                <td>邮箱</td>
                <td class="value">
                    <%= request.getAttribute("email") != null ? request.getAttribute("email") : "<span class='empty-value'>未填写</span>" %>
                </td>
            </tr>
            <tr>
                <td>手机号</td>
                <td class="value">
                    <%
                        String phone = (String) request.getAttribute("phone");
                        if (phone != null && !phone.isEmpty()) {
                            out.print(phone);
                        } else {
                            out.print("<span class='empty-value'>未填写</span>");
                        }
                    %>
                </td>
            </tr>
            <tr>
                <td>性别</td>
                <td class="value">
                    <%
                        String gender = (String) request.getAttribute("gender");
                        if (gender != null && !gender.isEmpty()) {
                            out.print(gender);
                        } else {
                            out.print("<span class='empty-value'>未选择</span>");
                        }
                    %>
                </td>
            </tr>
            <tr>
                <td>地址</td>
                <td class="value">
                    <%
                        String address = (String) request.getAttribute("address");
                        if (address != null && !address.isEmpty()) {
                            out.print(address);
                        } else {
                            out.print("<span class='empty-value'>未填写</span>");
                        }
                    %>
                </td>
            </tr>
        </table>

        <div class="btn-group">
            <a href="index.html" class="btn btn-primary">返回表单</a>
            <button onclick="window.print()" class="btn btn-secondary">打印此页</button>
        </div>
    </div>
</body>
</html>
