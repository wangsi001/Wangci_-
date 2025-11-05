package com.example.servlet;

import com.example.model.User;
import com.example.service.UserService;
import com.google.gson.Gson;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@WebServlet("/api/users/*")
public class UserServlet extends HttpServlet {
    private final UserService userService = new UserService();
    private final Gson gson = new Gson();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("application/json;charset=UTF-8");

        String pathInfo = request.getPathInfo();

        if (pathInfo == null || pathInfo.equals("/")) {
            List<User> users = userService.getAllUsers();
            response.getWriter().print(gson.toJson(users));
        } else {
            try {
                Long id = Long.parseLong(pathInfo.substring(1));
                User user = userService.getUserById(id);
                if (user != null) {
                    response.getWriter().print(gson.toJson(user));
                } else {
                    response.setStatus(404);
                    response.getWriter().print("{\"error\":\"User not found\"}");
                }
            } catch (NumberFormatException e) {
                response.setStatus(400);
                response.getWriter().print("{\"error\":\"Invalid ID\"}");
            }
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("application/json;charset=UTF-8");
        request.setCharacterEncoding("UTF-8");

        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = request.getReader().readLine()) != null) {
            sb.append(line);
        }

        User user = gson.fromJson(sb.toString(), User.class);
        User savedUser = userService.addUser(user);
        response.setStatus(201);
        response.getWriter().print(gson.toJson(savedUser));
    }
}
