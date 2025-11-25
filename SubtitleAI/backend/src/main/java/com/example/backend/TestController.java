package com.example.backend;

import java.util.Map;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@CrossOrigin(origins="*")
public class TestController {
    @GetMapping("/api/hello")
    public Map<String,String> hello(){
        return Map.of("msg","연결 성공!");
    }
}
