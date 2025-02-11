# C to ePL Compiler v1.2.2

## Introduction

### What is the C to ePL Compiler?

**c-to-epl** is a code converter that allows you to transform C algorithms into the **ePL language**, which is used on the **XEL network**. 

Since **ePL does not support function return values or function arguments**, writing code in it can be challenging. **c-to-epl** simplifies this process by automatically converting your C code to a compatible ePL format.

## 🚀 What's New in v1.2.2?
- ✅ Improved stability and bug fixes.
- ✅ Performance optimizations.
- ✅ Minor improvements in code conversion logic.

## 🚨 Known Issues & Limitations

**c-to-epl** is still a work in progress and may contain bugs. The following features are currently **not supported**:

- ❌ **Array initialization** is not allowed.
- ❌ You can only use **one function call per statement** (either standalone or in a variable assignment). More complex expressions **will fail**.
- ❌ **Pointers are not supported**.
- ❌ **Structs, enums, and typedefs** are not available.
- ❌ **Variable reuse in different scopes** is currently broken.
- ⚠️ **Other unexpected issues may arise**. If you encounter a bug, please **submit an issue or pull request** on GitHub.

## 💡 Contributing

We welcome contributions! If you find a bug or want to improve the compiler, feel free to:

1. Fork the repository.
2. Create a new branch.
3. Submit a pull request with your changes.

---

🔗 **GitHub Repository**: [xel-software/xel-c-to-epl-compiler](https://github.com/xel-software/xel-c-to-epl-compiler)  
📧 **Contact**: support@xel-software.com
