package com.example;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/submitForm")
public class FormServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");

        // 获取表单参数
        String name = request.getParameter("name");
        String age = request.getParameter("age");
        String email = request.getParameter("email");
        String phone = request.getParameter("phone");
        String gender = request.getParameter("gender");
        String address = request.getParameter("address");

        // 打印到控制台
        System.out.println("========== 表单数据 ==========");
        System.out.println("姓名: " + name);
        System.out.println("年龄: " + age);
        System.out.println("邮箱: " + email);
        System.out.println("手机号: " + phone);
        System.out.println("性别: " + gender);
        System.out.println("地址: " + address);
        System.out.println("==============================");

        // 传递数据到结果页面
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
        response.sendRedirect("index.html");
    }
}
