(define (domain robots)
  (:requirements :strips :typing)
  (:types robot hand person
          room cupholder tea-machine)
  (:constants
    EH EC FC - state
  )
  (:predicates
    (room-adjacent ?r1 ?r2 - room)
    (allowed-room ?rob - robot ?r - room)
    (at ?i - (either robot person cupholder tea-machine) ?r - room)
    (hand-state ?hs - state ?h - hand ?rob - robot)
    (served ?p - person)
  )

  (:action move-robot
    :parameters (?rob - robot ?r1 - room ?r2 - room)
    :precondition (and 
      (at ?rob ?r1)
      (room-adjacent ?r1 ?r2)
      (allowed-room ?rob ?r2)
    )
    :effect (and 
      (not (at ?rob ?r1))
      (at ?rob ?r2)
    )
  )

  (:action exchange
    :parameters (?rob1 - robot ?rob2 - robot ?r - room ?h1 - hand ?h2 - hand ?hs2 - state)
    :precondition (and 
      (at ?rob1 ?r)
      (at ?rob2 ?r)
      (hand-state EH ?h1 ?rob1)
      (hand-state ?hs2 ?h2 ?rob2)
    )
    :effect (and
      (not (hand-state EH ?h1 ?rob1))
      (not (hand-state ?hs2 ?h2 ?rob2))
      (hand-state ?hs2 ?h1 ?rob1)
      (hand-state EH ?h2 ?rob2)
    )
  )

  (:action serve
    :parameters (?rob - robot ?p - person ?h - hand ?r - room)
    :precondition (and
      (at ?rob ?r)
      (at ?p ?r)
      (hand-state FC ?h ?rob)
    )
    :effect (and
      (served ?p)
      (not (hand-state FC ?h ?rob))
      (hand-state EC ?h ?rob)
    )
  )

  (:action pick-empty-cup
    :parameters (?rob - robot ?r - room ?h - hand ?cp - cupholder)
    :precondition (and 
      (at ?rob ?r)
      (at ?cp ?r)
      (hand-state EH ?h ?rob)
    )
    :effect (and
      (not (hand-state EH ?h ?rob))
      (hand-state EC ?h ?rob)
    )
  )

  (:action fulfill-cup
    :parameters (?rob - robot ?r - room ?h - hand ?tm - tea-machine)
    :precondition (and 
      (at ?rob ?r)
      (at ?tm ?r)
      (hand-state EC ?h ?rob)
    )
    :effect (and
      (not (hand-state EC ?h ?rob))
      (hand-state FC ?h ?rob)
    )
  )
)