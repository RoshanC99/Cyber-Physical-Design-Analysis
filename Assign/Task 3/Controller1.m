function new_command = Controller1(previous_command, previous_state, current_state)
    % previous_command: a float, the last command to the blackbox
    % previous_state: a float, the previous position of the blackbox
    % current_state: a float, the current position of the blackbox
    %%%%% Do NOT modify anything outside this area %%%%%
    %%new_command = 0;
    
    % Using PID Controller Method, P - Kp and D - Kd
    % Based on Rule 3, previous_command is ignored 
    
    Kp = 0.5;
    Kd = 0.1;
    error = 0 - current_state;

    state_difference = current_state - previous_state;
    control_output = Kp*error - Kd*state_difference;

    if control_output > 0.25
        new_command = 1;
    elseif control_output < -0.25
        new_command = -1;
    else 
        new_command = 0;
    end 
    %%%%% Do NOT modify anything outside this area %%%%%
end