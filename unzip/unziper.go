package unzip

import (
    "fmt"
    "os"
    "archive/zip"
    "path/filepath"
    "log"
    "io"
)

func Unzip(path string, file os.FileInfo, dest string) error {
    fmt.Println(file.Name())
    zipreader, err := zip.OpenReader(path)
    if err != nil {
        log.Println(err)
        return err
    }

    defer zipreader.Close()

    for _, f := range zipreader.File {
        rc, err := f.Open()
        defer rc.Close()
        if err != nil {
            log.Println(err)
            return err
        }

        os.MkdirAll(dest, 0777)

        unzipfile, err := os.Create(filepath.Join(dest, f.Name)) 
        if err != nil {
            log.Println(err)
            return err
        }

        defer unzipfile.Close()

        if _, err := io.Copy(unzipfile, rc); err != nil {
            log.Println(err)
            return err
        }
    }

    return nil
}