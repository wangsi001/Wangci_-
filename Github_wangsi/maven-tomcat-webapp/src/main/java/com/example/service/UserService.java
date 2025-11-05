package com.example.service;

import com.example.model.User;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * 用户服务类
 * 提供用户的CRUD操作（使用内存存储作为示例）
 */
public class UserService {

    // 使用ConcurrentHashMap模拟数据库存储
    private static final Map<Long, User> userDatabase = new ConcurrentHashMap<>();
    private static final AtomicLong idGenerator = new AtomicLong(1);

    // 初始化一些测试数据
    static {
        User user1 = new User(idGenerator.getAndIncrement(), "张三", "zhangsan@example.com", "123456", 25, "13800138000");
        User user2 = new User(idGenerator.getAndIncrement(), "李四", "lisi@example.com", "123456", 28, "13900139000");
        User user3 = new User(idGenerator.getAndIncrement(), "王五", "wangwu@example.com", "123456", 30, "13700137000");

        userDatabase.put(user1.getId(), user1);
        userDatabase.put(user2.getId(), user2);
        userDatabase.put(user3.getId(), user3);
    }

    /**
     * 获取所有用户
     */
    public List<User> getAllUsers() {
        return new ArrayList<>(userDatabase.values());
    }

    /**
     * 根据ID获取用户
     */
    public User getUserById(Long id) {
        return userDatabase.get(id);
    }

    /**
     * 添加用户
     */
    public User addUser(User user) {
        if (user.getId() == null) {
            user.setId(idGenerator.getAndIncrement());
        }
        userDatabase.put(user.getId(), user);
        return user;
    }

    /**
     * 更新用户
     */
    public User updateUser(User user) {
        if (user.getId() == null) {
            throw new IllegalArgumentException("用户ID不能为空");
        }

        User existingUser = userDatabase.get(user.getId());
        if (existingUser == null) {
            throw new IllegalArgumentException("用户不存在");
        }

        userDatabase.put(user.getId(), user);
        return user;
    }

    /**
     * 删除用户
     */
    public void deleteUser(Long id) {
        User removed = userDatabase.remove(id);
        if (removed == null) {
            throw new IllegalArgumentException("用户不存在");
        }
    }

    /**
     * 根据用户名查找用户
     */
    public User getUserByUsername(String username) {
        return userDatabase.values().stream()
                .filter(user -> user.getUsername().equals(username))
                .findFirst()
                .orElse(null);
    }

    /**
     * 验证用户登录
     */
    public boolean validateUser(String username, String password) {
        User user = getUserByUsername(username);
        return user != null && user.getPassword().equals(password);
    }

    /**
     * 获取用户总数
     */
    public int getUserCount() {
        return userDatabase.size();
    }
}
