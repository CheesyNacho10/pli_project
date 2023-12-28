(define (domain robots)
  (:requirements :strips :typing)
  (:types robot hand person
          room cupholder tea-machine)
  (:predicates
    (room-adjacent ?r1 - room ?r2 - room)
    (allowed-room ?rob - robot ?r - room)
    (at_robot ?i - robot ?r - room)
    (at_person ?i - person ?r - room)
    (at_cupholder ?i - cupholder ?r - room)
    (at_teamachine ?i - tea-machine ?r - room)
    (empty ?h - hand ?rob - robot)
    (empty-cup ?h - hand ?rob - robot)
    (full-cup ?h - hand ?rob - robot)
    (served ?p - person)
  )

  (:action move-robot
    :parameters (?rob - robot ?r1 - room ?r2 - room)
    :precondition (and 
      (at_robot ?rob ?r1)
      (room-adjacent ?r1 ?r2)
      (allowed-room ?rob ?r2)
    )
    :effect (and 
      (not (at_robot ?rob ?r1))
      (at_robot ?rob ?r2)
    )
  )

  (:action exchange-empty
    :parameters (?rob1 - robot ?rob2 - robot ?r - room ?h1 - hand ?h2 - hand)
    :precondition (and 
      (at_robot ?rob1 ?r)
      (at_robot ?rob2 ?r)
      (empty-cup ?h1 ?rob1)
      (empty ?h2 ?rob2)
    )
    :effect (and
      (not (empty-cup ?h1 ?rob1))
      (not (empty ?h2 ?rob2))
      (empty-cup ?h2 ?rob2)
      (empty ?h1 ?rob1)
    )
  )

  (:action exchange-full
    :parameters (?rob1 - robot ?rob2 - robot ?r - room ?h1 - hand ?h2 - hand)
    :precondition (and 
      (at_robot ?rob1 ?r)
      (at_robot ?rob2 ?r)
      (full-cup ?h1 ?rob1)
      (empty ?h2 ?rob2)
    )
    :effect (and
      (not (full-cup ?h1 ?rob1))
      (not (empty ?h2 ?rob2))
      (full-cup ?h2 ?rob2)
      (empty ?h1 ?rob1)
    )
  )

  (:action serve
    :parameters (?rob - robot ?p - person ?h - hand ?r - room)
    :precondition (and
      (at_robot ?rob ?r)
      (at_person ?p ?r)
      (full-cup ?h ?rob)
    )
    :effect (and
      (served ?p)
      (not (full-cup ?h ?rob))
      (empty-cup ?h ?rob)
    )
  )

  (:action pick-empty-cup
    :parameters (?rob - robot ?r - room ?h - hand ?cp - cupholder)
    :precondition (and 
      (at_robot ?rob ?r)
      (at_cupholder ?cp ?r)
      (empty ?h ?rob)
    )
    :effect (and
      (not (empty ?h ?rob))
      (empty-cup ?h ?rob)
    )
  )

  (:action fulfill-cup
    :parameters (?rob - robot ?r - room ?h - hand ?tm - tea-machine)
    :precondition (and 
      (at_robot ?rob ?r)
      (at_teamachine ?tm ?r)
      (empty-cup ?h ?rob)
    )
    :effect (and
      (not (empty-cup ?h ?rob))
      (full-cup ?h ?rob)
    )
  )
)