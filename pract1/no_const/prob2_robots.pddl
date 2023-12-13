(define (problem probrobots)
    (:domain robots)
    (:objects
        P1 P2 P3 P4 - person
        ROB1 ROB2 ROB3 - robot
        HL HR - hand
        PAS R1 R2 R3 R4 - room
        TM - tea-machine
        CH - cupholder
    )
    (:init
        (room-adjacent PAS R1) (room-adjacent R1 PAS)
        (room-adjacent PAS R2) (room-adjacent R2 PAS)
        (room-adjacent PAS R3) (room-adjacent R3 PAS)
        (room-adjacent PAS R4) (room-adjacent R4 PAS)
        (room-adjacent R1 R2) (room-adjacent R2 R1)
        (room-adjacent R3 R4) (room-adjacent R4 R3)

        (allowed-room ROB1 PAS)
        (allowed-room ROB1 R1)
        (allowed-room ROB1 R2)

        (allowed-room ROB3 PAS)
        (allowed-room ROB3 R1)
        (allowed-room ROB3 R2)

        (allowed-room ROB2 PAS)
        (allowed-room ROB2 R3)
        (allowed-room ROB2 R4)

        (at ROB1 R1) (at ROB2 R3)
        (at ROB3 R2)
        (at P1 R2) (at P2 R3)
        (at P3 R2) (at P4 R4)

        (at TM R1) (at CH R3)

        (empty HL ROB1) (empty HR ROB1)
        (empty HL ROB2) (empty HR ROB2)
        (empty HL ROB3) (empty HR ROB3)
    )
    (:goal
        (and 
            (served P1)
            (served P2)
            (served P3)
            (served P4)
        )
    )
)
