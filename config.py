#!/usr/bin/python
# -*- coding: UTF-8 -*-

events = ['19714', '19715', '19716', '19717', '19718', '19719', '19720',
          '19722', '19723', '19724', '19725', '19726', '19727', '19728',
          '19730', '19731', '19732', '19733', '19734', '19735', '19736',
          '19738', '19739', '19740', '19741', '19742', '19743', '19744',
          '19745', '19746', '19747', '19748', '19749', '19750', '19751',
          '19752', '19753', '19759', '19760', '19761', '19762', '19763',
          '19765', '19766', '19767', '19768', '7298', '7443', '7444', '7445',
          '7456', '7457', '7471', '7472', '7473', '7474', '7475', '7476',
          '7477', '7478', '7479', '7480', '7482', '7483', '7484', '7485',
          '7486', '7487', '7490', '7492', '7493', '7494', '7496', '7497',
          '7500', '7519', '7520', '7521', '7522', '7523', '7524', '7525',
          '7529', '7530', '7531', '7532', '7533', '7534', '7535', '7536',
          '7537', '7538', '7539', '7540', '7541', '7542', '7543', '7544',
          '7545', '7546', '7547', '7548', '7549', '7550', '7551', '7552',
          '7553', '7554', '7555', '7556', '7557', '7558', '7559', '7560',
          '7561', '7562', '7563', '7564', '7565', '7566', '7567', '7568',
          '7569', '7570', '7571', '7572', '7576', '7577', '7578', '7579',
          '7580', '7581', '7582', '7583', '7584', '7585', '7586', '8649',
          '8650', '8651', '8652', '8655', '8656', '8657', '8658']

teams = ['Iran', 'South Korea', 'Japan', 'Saudi Arabia', 'Australia',
         'Tunisia', 'Nigeria', 'Morocco', 'Senegal', 'Egypt',
         'Mexico', 'Costa Rica', 'Panama',
         'Brazil', 'Uruguay', 'Argentina', 'Colombia', 'Peru',
         'France', 'Portugal', 'Germany', 'Serbia', 'Poland', 'England',
         'Spain', 'Belgium', 'Iceland', 'Switzerland', 'Croatia', 'Denmark',
         'Sweden', 'Russia']

columns = ['timestamp', 'possession_team', 'player', 'play_pattern', 'duration',
           'under_pressure', 'length', 'angle', 'height', 'pass_backheel',
           'miscommunication', 'through_ball', 'cross', 'cut_back', 'switch',
           'shot_assist', 'goal_assist', 'start_location_x', 'start_location_y',
           'end_location_x', 'end_location_y']

data_col = ['start_location_x', 'start_location_y',
            'end_location_x', 'end_location_y',
            'height', 'length', 'angle']

players_col = ['player']
types_col = ['play_pattern']

play_patterns = {'Regular Play': 0, 'From Corner': 1, 'From Free Kick': 2, 'From Throw In': 3,
                 'Other': 4, 'From Counter': 5, 'From Goal Kick': 6, 'From Keeper': 7,
                 'From Kick Off': 8}
height_patterns = {'Ground Pass': 0, 'Low Pass': 1, 'High Pass': 2}

X = 120
Y = 90

pos_classes = {0: ['Right Midfield', 'Right Wing', 'Left Wing', 'Left Midfield',
                   'Left Attacking Midfield', 'Right Attacking Midfield'],
               1: ['Right Center Midfield', 'Left Defensive Midfield', 'Center Attacking Midfield',
                   'Right Defensive Midfield', 'Center Midfield', 'Center Defensive Midfield',
                   'Left Center Midfield'],
               2: ['Left Wing Back', 'Right Wing Back', 'Right Back', 'Left Back'],
               3: ['Right Center Back', 'Left Center Back', 'Center Back'],
               4: ['Goalkeeper'],
               5: ['Left Center Forward', 'Right Center Forward', 'Center Forward',
                   'Secondary Striker']
              }
