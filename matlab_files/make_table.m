function overview = compileCSVFiles()
    % Function to compile CSV files from a predefined directory into a single table
    % Outputs:
    %   overview - compiled data table with NaNs replaced by False (0)

    % Define the directory containing the CSV files
    dirPath = '../wiring/saved_orientations';

    % Get list of CSV files in the directory
    files = dir(fullfile(dirPath, '*.csv'));

    % Initialize an empty table
    compiledData = table();

    % Loop through each file and concatenate data
    for k = 1:length(files)
        % Read the CSV file
        filePath = fullfile(files(k).folder, files(k).name);
        dat = readtable(filePath);

        % Reset index and remove first row
        dat = renamevars(dat, ["Var1", "Var2"],["channel_name", dat{1, "Var2"}]);
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

    fig = uifigure;
    uit = uitable(fig,'Data', overview);
    overview
end
