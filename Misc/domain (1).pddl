;Header and description

(define (domain ABPaS_domain)

;remove requirements that are not needed
(:requirements :strips :typing :fluents :negative-preconditions :disjunctive-preconditions)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
    (Is_Start ?s)              ;true iff start command is passed
    (Is_Stop ?st)              ;true iff stop command is passed
    (Is_Both_IR ?b)            ;true iff both left and right IR sensors are sensing input
    (Is_Left_IR ?x)            ;true iff only left IR sensor is sensing input
    (Is_Right_IR ?y)           ;true iff only right IR sensor is sensing input  
    (Is_Ultrasonic ?u)         ;true iff ultrasonic value sensor is less than 10 cm. 
    (Is_No_Ultrasonic ?u)      ;true iff ultrasonic value sensor is more than 10 cm. 
    (Is_Pir_Motion ?l)         ;true iff PIR motion value is 1.
    (Is_HighTemp ?t)           ;true iff temperature value is more than or equal 35 deg C.
    (Is_No_HighTemp ?t)        ;true iff temperature value is less than 35 deg C.
    (Move_Forward ?r)          ;true iff move forward and door action effect is achieved. Door is opened
    (Move_Left ?r)             ;true iff move left action effect is achieved.
    (Move_Right ?r)            ;true iff move right action effect is achieved.
    (Move_Stop ?r)             ;true iff move stop action effect is achieved.
    (Emermove_Stop ?r)         ;true iff emergency stop action effect is achieved. Buzzer is buzzed
    (Parking_Led_Glow ?p)      ;true iff parking led glow action effect is achieved.
    (Exhaust_Fan ?e)           ;true iff exhaust fan action effect is achieved.
    (Door_Motor ?d)
    )

;define actions here
(:action PIR_Detection
    :parameters (?l ?p ?t)
    :precondition (and (Is_Pir_Motion ?l) (Is_No_HighTemp ?t))
    :effect (Parking_Led_Glow ?p)    
)

;define actions here
(:action High_Temp_Detection
    :parameters (?t ?e)
    :precondition (Is_HighTemp ?t)
    :effect (Exhaust_Fan ?e)    
)

;define actions here
(:action Door_Motion
    :parameters (?s ?r ?t)
    :precondition (and (Is_Start ?s) (Is_No_HighTemp ?t))
    :effect (Door_Motor ?r)
)

;define actions here
(:action Forward_Motion
    :parameters (?b ?s ?u ?r ?t ?d)
    :precondition (and 
        (Is_Both_IR ?b)
        (Is_Start ?s)
        (Is_No_Ultrasonic ?u)
        (Is_No_HighTemp ?t)
        )
    :effect (Move_Forward ?r))

;define actions here
(:action Right_Motion
    :parameters (?x ?y ?s ?u ?r ?t)
    :precondition (and 
        (Is_Right_IR ?y)
        (Is_Start ?s)
        (Is_No_Ultrasonic ?u)
        (Is_No_HighTemp ?t)
        )
    :effect (Move_Right ?r)
)

;define actions here
(:action Left_Motion
    :parameters (?x ?y ?s ?u ?r ?t)
    :precondition (and 
        (Is_Left_IR ?x)
        (Is_Start ?s)
        (Is_No_Ultrasonic ?u)
        (Is_No_HighTemp ?t)
        )
    :effect (Move_Left ?r)
)

;define actions here
(:action Stop_Motion
    :parameters (?st ?u ?r ?t)
    :precondition(and
        (Is_Stop ?st)
        (Is_No_Ultrasonic ?u)
        (Is_No_HighTemp ?t))
    :effect (Move_Stop ?r)
)

;define actions here
(:action EmerStop_Motion
    :parameters (?r ?u ?t)
    :precondition (or
        (Is_Ultrasonic ?u)
        (Is_HighTemp ?t)
        )
    :effect (Emermove_Stop ?r)
)

)
