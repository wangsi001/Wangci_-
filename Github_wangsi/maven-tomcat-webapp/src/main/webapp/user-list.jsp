<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="com.example.service.UserService" %>
<%@ page import="com.example.model.User" %>
<%@ page import="java.util.List" %>
<%
    UserService userService = new UserService();
    List<User> users = userService.getAllUsers();
%>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户管理</title>
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
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
        }

        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2.5em;
        }

        .stats {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }

        .stats h2 {
            font-size: 3em;
            margin-bottom: 5px;
        }

        .stats p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        th, td {
            padding: 15px;
            text-align: left;
        }

        th {
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 1px;
        }

        tbody tr {
            border-bottom: 1px solid #e0e0e0;
            transition: background-color 0.3s;
        }

        tbody tr:hover {
            background-color: #f8f9fa;
        }

        tbody tr:last-child {
            border-bottom: none;
        }

        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-small {
            padding: 5px 15px;
            font-size: 0.9em;
        }

        .btn-danger {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }

        .action-buttons {
            display: flex;
            gap: 10px;
        }

        .back-link {
            text-align: center;
            margin-top: 20px;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }

        .empty-state h3 {
            font-size: 1.5em;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>👥 用户管理系统</h1>

        <div class="stats">
            <h2><%= users.size() %></h2>
            <p>注册用户总数</p>
        </div>

        <% if (users.isEmpty()) { %>
            <div class="empty-state">
                <h3>暂无用户数据</h3>
                <p>系统中还没有注册用户</p>
            </div>
        <% } else { %>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>用户名</th>
                        <th>邮箱</th>
                        <th>年龄</th>
                        <th>电话</th>
                        <th>创建时间</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <% for (User user : users) { %>
                        <tr>
                            <td><%= user.getId() %></td>
                            <td><%= user.getUsername() %></td>
                            <td><%= user.getEmail() %></td>
                            <td><%= user.getAge() != null ? user.getAge() : "-" %></td>
                            <td><%= user.getPhone() != null ? user.getPhone() : "-" %></td>
                            <td><%= user.getCreateTime() != null ? user.getCreateTime().toString().substring(0, 19) : "-" %></td>
                            <td>
                                <div class="action-buttons">
                                    <button class="btn btn-small" onclick="viewUser(<%= user.getId() %>)">查看</button>
                                    <button class="btn btn-small btn-danger" onclick="deleteUser(<%= user.getId() %>)">删除</button>
                                </div>
                            </td>
                        </tr>
                    <% } %>
                </tbody>
            </table>
        <% } %>

        <div class="back-link">
            <a href="index.jsp" class="btn">返回首页</a>
            <a href="user/list" class="btn">查看JSON API</a>
        </div>
    </div>

    <script>
        function viewUser(userId) {
            fetch('/user/' + userId)
                .then(response => response.json())
                .then(data => {
                    alert('用户信息：\n' + JSON.stringify(data, null, 2));
                })
                .catch(error => {
                    alert('获取用户信息失败：' + error);
                });
        }

        function deleteUser(userId) {
            if (confirm('确定要删除该用户吗？')) {
                fetch('/user/' + userId, {
                    method: 'DELETE'
                })
                .then(response => {
                    if (response.ok) {
                        alert('用户删除成功');
                        location.reload();
                    } else {
                        alert('删除失败');
                    }
                })
                .catch(error => {
                    alert('删除失败：' + error);
                });
            }
        }
    </script>
</body>
</html>
