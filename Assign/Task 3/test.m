% run the blackboxes once
% states1 contains the response from Blackbox1 for 1000 iterations
% states2 contains the response from Blackbox2 for 1000 iterations
[states1, states2] = run();

% set the tolerance for each blackbox
tolerance1 = 1;
tolerance2 = 20;

% generate plots
subplot(2,1,1)
plot(states1)
line([0 1000],[tolerance1 tolerance1],'color','r')
line([0 1000],[-tolerance1 -tolerance1],'color','r')
grid on
title('Blackbox 1 Response')

subplot(2,1,2)
plot(states2)
line([0 1000],[tolerance2 tolerance2],'color','r')
line([0 1000],[-tolerance2 -tolerance2],'color','r')
grid on
title('Blackbox 2 Response')

% run the blackboxes for 100 times and compute the final grade
[grade_blackbox1, grade_blackbox2, final_grade] = grade(tolerance1, tolerance2);
disp("Final grade: "+string(final_grade))

function [grade_blackbox1, grade_blackbox2, final_grade] = grade(tolerance1, tolerance2)
    fail_count_1 = 0;
    fail_count_2 = 0;
    
    % repeat for 100 times
    for i=1:100
        % run both blackboxes
        [states1, states2] = run();
        
        % check violations for blackbox1
        if any(states1(501:1000) < -tolerance1) || any(states1(501:1000) > tolerance1)
            fail_count_1 = fail_count_1 + 1;
        end
        
        % check violations for blackbox2
        if any(states2(501:1000) < -tolerance2) || any(states2(501:1000) > tolerance2)
            fail_count_2 = fail_count_2 + 1;
        end            
    end
    
    % compute final grade out of 40 pts
    grade_blackbox1 = 20*(100-fail_count_1)/100;
    grade_blackbox2 = 20*(100-fail_count_2)/100;
    final_grade = grade_blackbox1 + grade_blackbox2;
end
