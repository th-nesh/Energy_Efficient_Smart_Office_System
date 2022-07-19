(define(domain covisstorage)

     ;remove requirements that are not needed
(:requirements :strips :typing :fluents :negative-preconditions :disjunctive-preconditions)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
    (Is_Occupied ?o)              ;true iff Zone is occupied
    (Is_Un_Occupied ?uo)          ;true iff Zone is unoccupied
    (Is_Temp_High ?th)            ;true iff Zone Heat_index is High
    (Is_Temp_Ideal ?ti)           ;true iff Zone Heat_index is Ideal
    (Is_Temp_Low ?tl)             ;true iff Zone Heat_index is Low
    (Is_Light_Bright ?lb)         ;true iff Zone Luminence is High 
    (Is_Light_Normal ?ln)         ;true iff Zone Luminence is Ideal 
    (Is_Light_Gloomy ?lg)         ;true iff Zone Luminence is Low
    (Is_CO2_critical ?cc)         ;true iff CO2 level is critical.
    (Is_CO2_sub_critical ?cs);true iff CO2 level is sub-critical.
    (Is_CO2_normal ?cn)           ;true iff CO2 level is normal.
    (AC_On ?ao)                   ;true iff AC is ON.
    (AC_Off ?aof)                 ;true iff AC is OFF.
    (Window_Open ?wo)             ;true iff Window is fully opened.
    (Window_Mid_Open ?wmo)        ;true iff Window is partially opened. 
    (Window_Closed ?wc)           ;true iff Window is Closed.
    (Heating_High ?hh)            ;true iff Heating control is kept High.
    (Heating_Medium ?hm)          ;true iff Heating control is kept Medium.
    (Heating_Off ?ho)             ;true iff Heating control is Off.
    (Blind_Open ?bo)                ;true iff Window Blind is fully opened.
    (Blind_Mid_Open ?bmo)           ;true iff Window Blind is partially opened. 
    (Blind_Closed ?bc)              ;true iff Window Blind is Closed.
    (Lights_On ?lo)               ;true iff Lights are ON.
    (Lights_Off ?lof)             ;true iff Lights are OFF.

    )

;define actions here
(:action AC_switched_ON
    :parameters (?th ?a ?o)
    :precondition (and (Is_Temp_High ?th) (Is_Occupied ?o))
    :effect (AC_On ?a)  
)

;define actions here
(:action AC_switched_OFF
    :parameters (?t ?a ?o)
    :precondition (or (and (or (Is_Temp_Ideal ?t) (Is_Temp_Low ?t)) 
                           (Is_Occupied ?o)) 
                      (Is_Un_Occupied ?o))
    :effect (AC_Off ?a)    
)

;define actions here
(:action Heating_to_High
    :parameters (?h ?tl ?o)
    :precondition (and (Is_Temp_Low ?tl)(Is_Occupied ?o))
    :effect (Heating_High ?h)
)

;define actions here
(:action Heating_to_Medium
    :parameters (?h ?ti ?o)
    :precondition (and (Is_Temp_Ideal ?ti) (Is_Occupied ?o))
    :effect (Heating_Medium ?h)
)

;define actions here
(:action Heating_to_Off
    :parameters (?h ?th ?o)
    :precondition (or (and (Is_Temp_High ?th)(Is_Occupied ?o)) (Is_Un_Occupied ?o))
    :effect (Heating_Off ?h)
)

;define actions here
(:action Windows_Open
    :parameters (?w ?o ?cc)
    :precondition (and
        (Is_CO2_critical ?cc )
        (Is_Occupied ?o)
        )
    :effect (Window_Open ?w))

;define actions here
(:action Windows_Partially_Open
    :parameters (?w  ?cs ?o)
    :precondition (and 
        (Is_CO2_sub_critical ?cs)
        (Is_Occupied ?o)
        )
    :effect (Window_Mid_Open ?w)
)

;define actions here
(:action Windows_Closed
    :parameters (?w ?o ?cn )
    :precondition (or (and 
        (Is_CO2_normal ?cn )
        (Is_Occupied ?o)) (Is_Un_Occupied ?o)
        )
    :effect (Window_Closed ?w)
)

;define actions here


;define actions here
(:action Blinds_Open
    :parameters (?b ?o ?l)
    :precondition 
        (and (or (Is_Light_Gloomy ?l ) (Is_Light_Normal ?l) ) (Is_Occupied ?o))
       
    :effect (Blind_Open ?b)
)

;define actions here
(:action Blinds_Closed
    :parameters (?b ?o ?lb)
    :precondition 
        (or (and (Is_Light_Bright ?lb) (Is_Occupied ?o) ) (Is_Un_Occupied ?o))
       
    :effect (Blind_Closed ?b)
)

;define actions here
(:action Lights_On
    :parameters (?l ?o ?lg)
    :precondition 
        (and (Is_Light_Gloomy ?lg ) (Is_Occupied ?o))
       
    :effect (Lights_On ?l)
)

;define actions here
(:action Lights_Off
    :parameters (?l ?o ?lb)
    :precondition 
        (or (and (or (Is_Light_Normal ?lb)(Is_Light_Bright ?lb))(Is_Occupied ?o) )
        (Is_Un_Occupied ?o) )
       
    :effect (Lights_Off ?l)
)

)
