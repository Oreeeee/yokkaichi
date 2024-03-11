package main

import "fmt"

type Server struct {
	ip   string
	port uint16
}

func main() {
	servers := []Server{{"127.0.0.1", 25565}, {"127.0.0.1", 25566}}
	fmt.Println("Hello World")
	for _, element := range servers {
		showIP(element)
	}
}

func showIP(server Server) {
	fmt.Printf("%v:%v\n", server.ip, server.port)
}
