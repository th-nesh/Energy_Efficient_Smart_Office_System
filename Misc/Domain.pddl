;Header and description

(define (domain Smart_Office)

;remove requirements that are not needed
(:requirements :strips :fluents :typing )

(:types 
    heat_index Occ_state Lighting CO2_index - object
    High Medium Low - heat_index
    High Medium Low - Occ_state
    High Medium Low - Lighting
    High Medium Low - CO2_index
    ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
)


(:functions ;todo: define numeric functions here
)

;define actions here

)