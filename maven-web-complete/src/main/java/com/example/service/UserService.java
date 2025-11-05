package com.example.service;

import com.example.model.User;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

public class UserService {
    private static final Map<Long, User> users = new ConcurrentHashMap<>();
    private static final AtomicLong idGen = new AtomicLong(1);

    static {
        users.put(1L, new User(1L, "张三", "zhangsan@example.com", 25));
        users.put(2L, new User(2L, "李四", "lisi@example.com", 28));
        users.put(3L, new User(3L, "王五", "wangwu@example.com", 30));
        idGen.set(4);
    }

    public List<User> getAllUsers() {
        return new ArrayList<>(users.values());
    }

    public User getUserById(Long id) {
        return users.get(id);
    }

    public User addUser(User user) {
        if (user.getId() == null) {
            user.setId(idGen.getAndIncrement());
        }
        users.put(user.getId(), user);
        return user;
    }
}
