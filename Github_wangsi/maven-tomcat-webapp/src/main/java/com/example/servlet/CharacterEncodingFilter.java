package com.example.servlet;

import jakarta.servlet.*;
import java.io.IOException;

/**
 * 字符编码过滤器
 * 确保所有请求和响应使用UTF-8编码
 */
public class CharacterEncodingFilter implements Filter {

    private String encoding = "UTF-8";

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        String encodingParam = filterConfig.getInitParameter("encoding");
        if (encodingParam != null && !encodingParam.trim().isEmpty()) {
            this.encoding = encodingParam;
        }
        System.out.println("CharacterEncodingFilter初始化，使用编码：" + encoding);
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        // 设置请求编码
        request.setCharacterEncoding(encoding);

        // 设置响应编码
        response.setCharacterEncoding(encoding);

        // 继续过滤器链
        chain.doFilter(request, response);
    }

    @Override
    public void destroy() {
        System.out.println("CharacterEncodingFilter被销毁");
    }
}
