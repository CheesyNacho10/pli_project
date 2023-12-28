(define (problem probrobots)
  (:domain robots)
  (:objects
    P1 P2 - person
    ROB1 ROB2 - robot
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

    (allowed-room ROB2 PAS)
    (allowed-room ROB2 R3)
    (allowed-room ROB2 R4)

    (at_robot ROB1 R1) (at_robot ROB2 R3)
    (at_person P1 R2) (at_person P2 R3)

    (at_teamachine TM R1) (at_cupholder CH R3)

    (empty HL ROB1) (empty HR ROB1)
    (empty HL ROB2) (empty HR ROB2)
  )
  (:goal
    (and 
      (served P1)
      (served P2)
    )
  )
)
