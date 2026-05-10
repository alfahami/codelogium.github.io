---
title: "Generic Types in Java"
date: 2025-05-07
description: "Explore how Java generics work across interfaces and classes."
categories:
  - Java
  - Programming
  - OOP
description: "Explore how Java generics work across interfaces, classes, and multi-type scenarios with real examples."
tags:
  - Generics
  - Type Safety
  - Interfaces
reading_time: 5
cover: /assets/images/generics-cover.png  # Optional: update with an actual image path
summary: |
  Dive deeper into Java generics through interfaces, key-value pairs, and multi-type generic classes. Understand how to apply them in real use cases like repositories and collections.
---

# Generic Types in Java

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By —<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/java/"><em>java</em></a>&nbsp;•&nbsp;  
         <a href="/categories/programming/"><em>programming</em></a>&nbsp;•&nbsp; 
         <a href="/categories/programming/"><em>oop</em></a>&nbsp;•&nbsp;  
      ⏱️ ~5 min read</span>
    </span>
  </div>
</div>

> “Write once, use many” — Generics let you write flexible and reusable code.

In short, *Generic Types* allow you to define interfaces, classes, or methods using a placeholder type that is specified later when the class or method is instantiated. This is common in Java Collections, like `List<String>`, `ArrayList<Integer>`, or `Map<Long, String>`.

??? note "Loosely Speaking"
    When using a single letter (e.g., `<T>`, `<E>`, or `<K, V>`) in `public interface <T> GenericInterface {}`, `public class GenericClass<T> {}`, or `public <T> genericMethod() {}`, you're essentially telling the user of your generic interface, class, or method that they can use any type they wish when instantiating it — even custom types.
    
One of the tricky parts of generics is seeing `<T>` sitting next to `void` or any other return type. At first, it feels like `<T>` is another return type, but it’s not. Instead, it’s just a signal to the compiler that `T` is a placeholder. Whenever you use the method, the compiler will replace `T` with the actual type you provide.
Generics allow you to write a class or method that operates on objects of various types — such as `Integer`, `String`, or custom classes — without rewriting the code for each type.

Generics in Java ensure type safety, reduce boilerplate, prevent runtime errors (like `ClassCastException`), and make the code easier to read and maintain.

According to the [official Java documentation](http://docs.oracle.com/javase/tutorial/java/generics/types.html):

<blockquote><p>A generic type is a generic class or interface that is parameterized over types.</p></blockquote>

You typically use a generic class when all its behavior (like its methods) should apply consistently to a single data type. A great example is the **Java Collections Framework** — such as `ArrayList<T>` and `HashMap<K, V>`.

In a generic class, you use a type parameter (e.g., `T`) to represent the data type. This allows you to write flexible and reusable code that can work with any type: `Integer`, `String`, `Double`, `Character`, or even user-defined types.

---

## Generic Classes

In generic classes, **static methods cannot use class-level type parameters.**<br>
You typically use a generic class when all its behavior (like its methods) should apply consistently to a single data type. A great example?<br>
Most of the **Java Collections Framework --** like `ArrayList<T>`, `HashMap<K,V>` are build with generics.

Here’s a simple generic class called `Box`:

```java
public class Box<T> {
    // T can be any type (Integer, String, Object, etc.)
    private T value;

    public void set(T value) {
        this.value = value;
    }

    public T get() {
        return value;
    }
}
```

This `Box` class can hold any type of object. For example:

```java
Box<String> stringBox = new Box<>();
stringBox.set("Hello");

Box<Integer> intBox = new Box<>();
intBox.set(123);
```

??? tip "Quite a Stretch"
    Imagine a strong iron box that can hold *any* kind of item — even ones crafted by the user themselves.<br>
    Now, let’s stretch that idea a bit further...

    What if this box could hold another box just like it? Could it nest within itself, over and over?

    The answer is: **yes**! <br> 
    That’s the idea behind recursive generics — a container that can hold its own kind.<br>  
    (But don’t worry — we won’t dive into that here.)
---

## Generic Methods

You can also create generic methods that work independently of any class being generic:

```java
public static class Utility {
    public static <T> void printArray(T[] array) {
        for (T element : array) {
            System.out.print(element + " ");
        }
    }
}
```

You could call this method with different types of arrays:

```java
Integer[] intArray = {1, 2, 3};
String[] stringArray = {"a", "b", "c"};

Utility.printArray(intArray);
Utility.printArray(stringArray);
```

!!! tip "Why Generics Matter"
    Generics catch type mismatches at **compile time**, helping you avoid `ClassCastException` errors and making your code more reliable.

---

## Advanced Uses of Generics in Java

### Generic Interfaces

Generics improve type safety and code reusability, ensuring compile-time checks and reducing runtime errors. You can define generic interfaces to operate on various types, improving flexibility and reuse:

```java
public interface InnerGenericType<T> {
    void save(T entity);
    T findByIndex(int id);
}
```

### Implementing a Generic Interface

```java
public class Utilisateur {
    private int id;
    private String username;

    public String getUsername() { return username; }
    public int getId() { return id; }
    public void setUsername(String username) { this.username = username; }
    public void setId(int id) { this.id = id; }
}

public class UserRepository implements InnerGenericType<Utilisateur> {
    ArrayList<Utilisateur> userRepository = new ArrayList<>();

    @Override
    public void save(Utilisateur user) {
        userRepository.add(user);
    }

    @Override
    public Utilisateur findByIndex(int id) {
        return userRepository.get(id);
    }
}
```

### Using `E` for Element in a Custom Collection

Adding `<E>` in the class definition defines the class as generic. The class can operate on objects of any type specified at the time of instantiation, rather than being tied to a specific type. `E` is a placeholder for the type you specify later when using the class.

```java
public class CustomList<E> {
    private List<E> elements = new ArrayList<>();

    public void setElement(E element) {
        elements.add(element);
    }

    public E getElement(int index) {
        return elements.get(index);
    }
}
```

This allows storage of elements of any type defined at the time of instantiation.

### Using `K` and `V` in a Key-Value Pair

```java
public static class KeyValue<K, V> {
    private K key;
    private V value;

    public KeyValue(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public K getKey() { return key; }
    public V getValue() { return value; }
    public void setKey(K key) { this.key = key; }
    public void setValue(V value) { this.value = value; }
}
```

### Combining `E`, `K`, and `V` in a Multi-Generic Class

```java
public static class MultiMap<K, V, E> {
    private E extra;
    private K key;
    private V value;

    public void put(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public K getKey() { return key; }
    public V getValue() { return value; }
    public E getExtra() { return extra; }
    public void setKey(K key) { this.key = key; }
    public void setValue(V value) { this.value = value; }
    public void setExtra(E extra) { this.extra = extra; }
}
```

### Example Usage in `main`

```java
// Generic Box that can hold String
Box<String> stringBox = new Box<>();
stringBox.setItem("Hello");
System.out.println(stringBox.getItem());

// Use Integer as type parameter
Box<Integer> integerBox = new Box<>();
integerBox.setItem(4321);
System.out.println(integerBox.getItem());

// Generic Method
String[] names = { "Alice", "Bob" };
Integer[] numbers = { 1, 2, 4 };
Utility.printArray(names);
Utility.printArray(numbers);

// Generic Interface
Utilisateur user = new Utilisateur();
UserRepository userRepo = new UserRepository();
user.setId(0);
user.setUsername("Djaloud");
userRepo.save(user);
System.out.println(userRepo.findByIndex(0).getUsername());

// Using Generics in Collections
List<String> list = new ArrayList<>();
list.add("Hello");
System.out.println(list.get(0));

// Using CustomList with E
CustomList<String> customStringList = new CustomList<>();
customStringList.setElement("Apple");
customStringList.setElement("Banana");

CustomList<Integer> customIntegerList = new CustomList<>();
customIntegerList.setElement(20);
customIntegerList.setElement(15);
System.out.println("The price of an " + customStringList.getElement(0) + " is " + customIntegerList.getElement(0));

// KeyValue
KeyValue<Integer, String> productPrice = new KeyValue<>(38500, "ASUS ProArt 16");
System.out.println("The model " + productPrice.getValue() + " costs " + productPrice.getKey() + " MAD");

KeyValue<String, Integer> ageMapping = new KeyValue<>("Akmal Eddine", 16);
System.out.println(ageMapping.getKey() + " is " + ageMapping.getValue() + " years old");

// MultiMap
MultiMap<String, Integer, String> fruitInfo = new MultiMap<>();
fruitInfo.put("Banana", 10);
fruitInfo.setExtra("imported from Morocco");
System.out.println("The " + fruitInfo.getKey() + " is " + fruitInfo.getValue() + " MAD and is " + fruitInfo.getExtra());
```

---

## What We Learned

Java generics allow us to write flexible, type-safe code. In this post, we explored how generic interfaces and classes enhance reusability and improve readability.

We also saw how Java Collections use generics under the hood and discussed **type erasure** at runtime.

The full Java file for this learning can be found here: [GenericType.java](https://github.com/codelogium/codelogium/blob/main/java/GenericType.java)

---

## Collateral Knowledge

??? info "Key Insights into Nested Interface and Self-Instatiating Classes in OOP"
    Along the way, we also discovered two interesting aspects of OOP:

    1. **Interfaces inside classes are implicitly static.**<br> 
    If you're declaring an interface inside a class, **you can** make it `static` — and **you usually should**, to avoid holding an implicit reference to the outer class.
    Interfaces declared inside a class are **implicitly static**, meaning they can be used without creating an instance of the outer class. And that's an interesting and sometimes subtle aspect of Java! <br>
    Even if you don’t explicitly use the static keyword, any interface declared inside a class is implicitly static by definition. This means you can reference it without creating an instance of the enclosing class, and it behaves independently of any specific instance of the outer class. An interface is implicitly `static` when declared inside a class. You don't need an instance of the outer class to use it.

    2. **Classes can instantiate themselves (and it’s totally valid)**<br>
    It's possible to instantiate a class from within itself in the `main` method (!like I'm creating this class, but I'm also instantiating this class in this class ... cool tho!) — something not usually needed but helpful when everything is enclosed in one file.
    Because we used a single Java class to contain all the examples, we had to reference generic classes and interfaces from within the same outer class. That’s where we learned this pattern:

        ```java
        public static void main(String[] args) {
            // We need an instance of the outer class to access inner non-static classes
            GenericType outerInstance = new GenericType();

            Box<String> stringBox = outerInstance.new Box<>();
            stringBox.setItem("Hello");
            System.out.println(stringBox.getItem());
        }
        ```
---
