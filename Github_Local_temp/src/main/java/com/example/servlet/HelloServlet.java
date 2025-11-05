package com.example.servlet;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * 简单的Hello World Servlet示例
 */
public class HelloServlet extends HttpServlet {

    @Override
    public void init() throws ServletException {
        super.init();
        System.out.println("HelloServlet初始化完成");
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        PrintWriter out = response.getWriter();

        String name = request.getParameter("name");
        if (name == null || name.trim().isEmpty()) {
            name = "访客";
        }

        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

        out.println("<!DOCTYPE html>");
        out.println("<html>");
        out.println("<head>");
        out.println("<title>Hello Servlet</title>");
        out.println("<meta charset='UTF-8'>");
        out.println("<style>");
        out.println("body { font-family: Arial, sans-serif; margin: 50px; background-color: #f0f0f0; }");
        out.println(".container { background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }");
        out.println("h1 { color: #333; }");
        out.println("p { color: #666; line-height: 1.6; }");
        out.println("a { color: #007bff; text-decoration: none; }");
        out.println("a:hover { text-decoration: underline; }");
        out.println("</style>");
        out.println("</head>");
        out.println("<body>");
        out.println("<div class='container'>");
        out.println("<h1>你好，" + name + "！</h1>");
        out.println("<p>欢迎来到Maven + Tomcat Web应用程序</p>");
        out.println("<p>当前时间：" + now.format(formatter) + "</p>");
        out.println("<p>服务器信息：" + getServletContext().getServerInfo() + "</p>");
        out.println("<hr>");
        out.println("<p><a href='index.jsp'>返回首页</a> | <a href='hello?name=张三'>测试参数</a> | <a href='user/list'>用户列表</a></p>");
        out.println("</div>");
        out.println("</body>");
        out.println("</html>");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doGet(request, response);
    }

    @Override
    public void destroy() {
        System.out.println("HelloServlet被销毁");
        super.destroy();
    }
}
