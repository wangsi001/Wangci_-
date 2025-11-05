package com.example;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * 表单处理Servlet
 * 接收表单数据，打印到控制台，转发到结果页面
 */
@WebServlet("/submitForm")
public class FormServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        // 设置请求编码为UTF-8，防止中文乱码
        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");

        // 获取表单参数
        String name = request.getParameter("name");
        String age = request.getParameter("age");
        String email = request.getParameter("email");
        String phone = request.getParameter("phone");
        String gender = request.getParameter("gender");
        String address = request.getParameter("address");

        // 打印到控制台（Tomcat日志）
        System.out.println("========== 接收到表单数据 ==========");
        System.out.println("姓名: " + name);
        System.out.println("年龄: " + age);
        System.out.println("邮箱: " + email);
        System.out.println("手机号: " + phone);
        System.out.println("性别: " + gender);
        System.out.println("地址: " + address);
        System.out.println("===================================");

        // 将参数存储到request作用域，传递给结果页面
        request.setAttribute("name", name);
        request.setAttribute("age", age);
        request.setAttribute("email", email);
        request.setAttribute("phone", phone);
        request.setAttribute("gender", gender);
        request.setAttribute("address", address);

        // 转发到结果页面
        request.getRequestDispatcher("/result.jsp").forward(request, response);
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        // 如果是GET请求，重定向到首页
        response.sendRedirect("index.html");
    }
}
