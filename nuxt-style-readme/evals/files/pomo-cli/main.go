package main

import (
	"flag"
	"fmt"
	"time"
)

func main() {
	work := flag.Duration("work", 25*time.Minute, "length of a work interval")
	brk := flag.Duration("break", 5*time.Minute, "length of a break")
	rounds := flag.Int("rounds", 4, "number of work intervals before a long break")
	notify := flag.Bool("notify", true, "send a desktop notification at each transition")
	flag.Parse()

	for i := 1; i <= *rounds; i++ {
		fmt.Printf("round %d/%d: work %s\n", i, *rounds, *work)
		time.Sleep(*work)
		if *notify {
			notifySend("break time")
		}
		time.Sleep(*brk)
	}
}
