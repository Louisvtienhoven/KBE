function overview = compileCSVFiles(dirPath)
    % Function to compile CSV files from a predefined directory into a single table
    % Outputs:
    % overview - compiled data table

    % Get list of CSV files in the directory
    files = dir(fullfile(dirPath, '*.csv'));

    % Initialize an empty table
    compiledData = table();

    % Loop through each file and concatenate data
    for k = 1:length(files)
        % Read the CSV file
        filePath = fullfile(files(k).folder, files(k).name);

        file = split(filePath, "_");

        angle = split(file(4), ".");
        angle = angle(1);

        opts = detectImportOptions(filePath);
        opts = setvartype(opts,'logical');

        idx = readtable(filePath);
        idx = idx(:,1);
        
        boolean = readtable(filePath, opts);
        boolean = boolean(:,2);

        dat = table();
        dat(:, 1) = idx;
        dat(:, 2) = boolean;

        % Reset index and remove first row
        dat = renamevars(dat, ["Var1", "Var2"],["channel_name", angle]);
        dat(1,:) = [];

        % If the compiledData is empty, initialize it with the first table
        if isempty(compiledData)
            compiledData = dat;
        else
            rowNames = unique([dat.Row; compiledData.Row]);

            % Join the tables on the row names
            compiledData = outerjoin(compiledData, dat,'MergeKeys', true, 'Type', 'full');
        end
    end

    % Replace NaNs with false (0)
    % Iterate through each element of the table
    for i = 1:height(compiledData)
        for j = 1:width(compiledData)
            if iscell(compiledData{i, j}) && isempty(compiledData{i, j}{1})
                compiledData{i, j} = {'False'};
            elseif ischar(compiledData{i, j}) && isempty(T{i, j})
                compiledData{i, j} = 'False';
            end
        end
    end

    % Output the compiled table
    overview = compiledData;

    engine = str2num(char(file(3))) + 1;
    engineStage = file(2);
    engineStage = split(engineStage, "\");
    engineStage = str2num(char(engineStage(4))) + 1;

    engineStageNames = ["Fan", "LP compressor", "HP compressor", "HP turbine", "LP turbine"];

    engineNames = ["Left", "Right"];

    fig = uifigure;
    lbl = uilabel(fig);

    lblFormat = "Rotor burst overview of the %s of the %s engine";
    lbl.Text = sprintf(lblFormat, engineStageNames(engineStage), engineNames(engine));
    lbl.Position = [100 0 100 200];
    lbl.WordWrap = "on";
    uit = uitable(fig,'Data', overview, "Position",[100 200 100 100]);

    filenameFormat ='../wiring/saved_orientations/report_%s_%s.xlsx';
    writetable(overview, sprintf(filenameFormat,engineNames(engine), engineStageNames(engineStage)));

end
