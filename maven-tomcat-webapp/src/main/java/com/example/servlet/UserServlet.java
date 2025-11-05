package com.example.servlet;

import com.example.model.User;
import com.example.service.UserService;
import com.google.gson.Gson;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

/**
 * 用户管理Servlet
 * 支持RESTful风格的请求处理
 */
public class UserServlet extends HttpServlet {

    private UserService userService;
    private Gson gson;

    @Override
    public void init() throws ServletException {
        super.init();
        userService = new UserService();
        gson = new Gson();
        System.out.println("UserServlet初始化完成");
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String pathInfo = request.getPathInfo();
        response.setContentType("application/json;charset=UTF-8");

        if (pathInfo == null || pathInfo.equals("/") || pathInfo.equals("/list")) {
            // 获取所有用户列表
            handleGetAllUsers(response);
        } else {
            // 获取特定用户
            String userId = pathInfo.substring(1);
            handleGetUser(userId, response);
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("application/json;charset=UTF-8");

        // 从请求体读取JSON数据
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = request.getReader().readLine()) != null) {
            sb.append(line);
        }

        try {
            User user = gson.fromJson(sb.toString(), User.class);
            userService.addUser(user);

            response.setStatus(HttpServletResponse.SC_CREATED);
            PrintWriter out = response.getWriter();
            out.print(gson.toJson(user));
        } catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            PrintWriter out = response.getWriter();
            out.print("{\"error\": \"" + e.getMessage() + "\"}");
        }
    }

    @Override
    protected void doPut(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("application/json;charset=UTF-8");

        String pathInfo = request.getPathInfo();
        if (pathInfo == null || pathInfo.equals("/")) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }

        String userId = pathInfo.substring(1);

        // 从请求体读取JSON数据
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = request.getReader().readLine()) != null) {
            sb.append(line);
        }

        try {
            User user = gson.fromJson(sb.toString(), User.class);
            user.setId(Long.parseLong(userId));
            userService.updateUser(user);

            PrintWriter out = response.getWriter();
            out.print(gson.toJson(user));
        } catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            PrintWriter out = response.getWriter();
            out.print("{\"error\": \"" + e.getMessage() + "\"}");
        }
    }

    @Override
    protected void doDelete(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("application/json;charset=UTF-8");

        String pathInfo = request.getPathInfo();
        if (pathInfo == null || pathInfo.equals("/")) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }

        String userId = pathInfo.substring(1);

        try {
            userService.deleteUser(Long.parseLong(userId));
            response.setStatus(HttpServletResponse.SC_NO_CONTENT);
        } catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            PrintWriter out = response.getWriter();
            out.print("{\"error\": \"" + e.getMessage() + "\"}");
        }
    }

    private void handleGetAllUsers(HttpServletResponse response) throws IOException {
        List<User> users = userService.getAllUsers();
        PrintWriter out = response.getWriter();
        out.print(gson.toJson(users));
    }

    private void handleGetUser(String userId, HttpServletResponse response) throws IOException {
        try {
            User user = userService.getUserById(Long.parseLong(userId));
            if (user != null) {
                PrintWriter out = response.getWriter();
                out.print(gson.toJson(user));
            } else {
                response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                PrintWriter out = response.getWriter();
                out.print("{\"error\": \"User not found\"}");
            }
        } catch (NumberFormatException e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            PrintWriter out = response.getWriter();
            out.print("{\"error\": \"Invalid user ID\"}");
        }
    }
}
