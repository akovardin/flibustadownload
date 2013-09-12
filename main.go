package main

import (
    "fmt"
    "os"
    "path/filepath"
    "./unzip"
)

func main() {
    folder := "./"
    dest := "./"

    if len(os.Args) > 1 {
        folder = os.Args[1]
    }

    if len(os.Args) > 2 {
        dest = os.Args[2]
    }

    fmt.Println("start")
    filepath.Walk(folder, func (path string, file os.FileInfo, err error) error {
        fmt.Println("Visited: %s", path)
        unzip.Unzip(path, file, dest) 
        return nil
    })
}