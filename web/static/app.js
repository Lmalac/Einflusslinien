const spanCountSelect =
    document.getElementById("span-count");

const spanInputsContainer =
    document.getElementById("span-inputs");

const totalLengthElement =
    document.getElementById("total-length");

const separatorsContainer =
    document.getElementById("separators-container");

const dimensionsContainer =
    document.getElementById("dimensions-container");

const endsContainer =
    document.getElementById("ends-container");

const supportsContainer =
    document.getElementById("supports-container");

const hingesContainer =
    document.getElementById("hinges-container");

const hingesPanel =
    document.getElementById("hinges");

const intermediateSupportsContainer =
    document.getElementById("intermediate-supports");

const leftSupportSelect =
    document.getElementById("left-support");

const rightSupportSelect =
    document.getElementById("right-support");

const buildSchemeButton =
    document.getElementById("build-scheme-button");
const influenceQuantity = document.getElementById("influence-quantity");
const influenceSection = document.getElementById("influence-section");
const influenceSectionLabel = document.getElementById("influence-section-label");
const influenceSupportLabel = document.getElementById("influence-support-label");
const influenceSupport = document.getElementById("influence-support");
const calculateInfluenceButton = document.getElementById("calculate-influence-button");
const influenceResult = document.getElementById("influence-result");


let spanLengthInputs = [];
let spanEiInputs = [];

let intermediateSupportSelects = [];

let hingePositionInputs = [];
let currentSchemeData = null;
let schemeRevision = 0;
let influenceRequestId = 0;


function clearInfluenceResult() {
    influenceRequestId += 1;
    influenceResult.replaceChildren();
}


function setSchemeWarning(visible) {
    const result = document.getElementById("scheme-result");
    let warning = result.querySelector("#scheme-warning");
    if (!visible) {
        warning?.remove();
        return;
    }
    if (!warning) {
        warning = document.createElement("div");
        warning.id = "scheme-warning";
        warning.setAttribute("role", "alert");
        warning.textContent = "Схема балки изменяема, измените схему";
        result.appendChild(warning);
    }
}


function isChangeableSchemeError(message) {
    return /изменяем|вырожден|механизм/i.test(String(message));
}


function invalidateSchemeResults() {
    schemeRevision += 1;
    currentSchemeData = null;
    calculateInfluenceButton.disabled = true;
    influenceSupport.replaceChildren();
    document.getElementById("scheme-result").textContent = "";
    setSchemeWarning(false);
    clearInfluenceResult();
}


function createSpanInputs() {

    spanInputsContainer.innerHTML = "";

    spanLengthInputs = [];
    spanEiInputs = [];

    const count =
        Number(spanCountSelect.value);


    for (let i = 0; i < count; i++) {

        const row =
            document.createElement("div");

        row.className = "span-row";


        const lengthLabel =
            document.createElement("label");

        lengthLabel.textContent =
            `Пролёт ${i + 1}: L =`;


        const lengthInput =
            document.createElement("input");

        lengthInput.type = "number";
        lengthInput.min = "0.5";
        lengthInput.step = "0.1";
        lengthInput.value = "6.0";


        lengthInput.addEventListener(
            "input",
            updateBeam
        );


        spanLengthInputs.push(
            lengthInput
        );


        const lengthUnit =
            document.createElement("span");

        lengthUnit.className = "unit";
        lengthUnit.textContent = "м";


        const eiLabel =
            document.createElement("label");

        eiLabel.textContent =
            "   EI =";


        const eiInput =
            document.createElement("input");

        eiInput.type = "number";
        eiInput.min = "0.01";
        eiInput.step = "0.1";
        eiInput.value = "1.0";


        spanEiInputs.push(
            eiInput
        );


        const eiUnit =
            document.createElement("span");

        eiUnit.className = "unit";
        eiUnit.textContent = "(относительная)";


        row.appendChild(lengthLabel);
        row.appendChild(lengthInput);
        row.appendChild(lengthUnit);

        row.appendChild(eiLabel);
        row.appendChild(eiInput);
        row.appendChild(eiUnit);


        spanInputsContainer.appendChild(row);
    }


    createIntermediateSupports();
    createHingeInputs();

    updateBeam();
}


function createIntermediateSupports() {

    intermediateSupportSelects = [];

    intermediateSupportsContainer.innerHTML = "";


    const count =
        Number(spanCountSelect.value);


    if (count <= 1) {
        return;
    }


    const title =
        document.createElement("div");

    title.className =
        "intermediate-title";

    title.textContent =
        "Средние опоры:";

    intermediateSupportsContainer.appendChild(
        title
    );


    for (let i = 0; i < count - 1; i++) {

        const row =
            document.createElement("div");

        row.className =
            "intermediate-support-row";


        const label =
            document.createElement("label");

        label.textContent =
            `Опора между L${i + 1} и L${i + 2}:`;


        const select =
            document.createElement("select");


        const pinnedOption =
            document.createElement("option");

        pinnedOption.value =
            "pinned";

        pinnedOption.textContent =
            "Шарнирно-неподвижная";


        const rollerOption =
            document.createElement("option");

        rollerOption.value =
            "roller";

        rollerOption.textContent =
            "Шарнирно-подвижная";


        select.appendChild(
            pinnedOption
        );

        select.appendChild(
            rollerOption
        );


        select.addEventListener(
            "change",
            updateBeam
        );


        intermediateSupportSelects.push(
            select
        );


        row.appendChild(label);
        row.appendChild(select);


        intermediateSupportsContainer.appendChild(
            row
        );
    }
}


function createHingeInputs() {

    hingesPanel.innerHTML = "";

    hingePositionInputs = [];


    const row =
        document.createElement("div");

    row.className = "row";


    const label =
        document.createElement("label");

    label.textContent =
        "Количество внутренних шарниров:";


    const select =
        document.createElement("select");

    select.id =
        "hinge-count";


    for (let i = 0; i <= 5; i++) {

        const option =
            document.createElement("option");

        option.value = i;
        option.textContent = i;

        select.appendChild(option);
    }


    row.appendChild(label);
    row.appendChild(select);

    hingesPanel.appendChild(row);


    const positionsContainer =
        document.createElement("div");

    positionsContainer.id =
        "hinge-positions";

    hingesPanel.appendChild(
        positionsContainer
    );


    select.addEventListener(
        "change",
        function () {

            createHingePositionInputs(
                Number(select.value)
            );

            updateBeam();
        }
    );


    createHingePositionInputs(0);
}


function createHingePositionInputs(
    count
) {

    const positionsContainer =
        document.getElementById(
            "hinge-positions"
        );

    positionsContainer.innerHTML = "";

    hingePositionInputs = [];


    if (count === 0) {
        return;
    }


    const title =
        document.createElement("div");

    title.className =
        "hinge-title";

    title.textContent =
        "Координаты внутренних шарниров от левого края:";

    positionsContainer.appendChild(
        title
    );


    for (let i = 0; i < count; i++) {

        const row =
            document.createElement("div");

        row.className =
            "hinge-row";


        const label =
            document.createElement("label");

        label.textContent =
            `Шарнир ${i + 1}: X =`;


        const input =
            document.createElement("input");

        input.type = "number";
        input.min = "0.01";
        input.step = "0.1";


        const totalLength =
            getTotalLength();


        input.value =
            (
                (i + 1)
                * totalLength
                / (count + 1)
            ).toFixed(2);


        input.addEventListener(
            "input",
            updateBeam
        );


        const unit =
            document.createElement("span");

        unit.className = "unit";
        unit.textContent = "м";


        row.appendChild(label);
        row.appendChild(input);
        row.appendChild(unit);


        positionsContainer.appendChild(row);

        hingePositionInputs.push(input);
    }
}


function getSpanLengths() {

    return spanLengthInputs.map(
        input => Number(input.value)
    );
}


function getTotalLength() {

    return getSpanLengths().reduce(
        (sum, value) => sum + value,
        0
    );
}


function positionToPercent(
    position,
    totalLength
) {

    return (
        position / totalLength * 100
    );
}


function getIntermediateSupportPositions() {

    const positions = [];

    let currentPosition = 0;


    for (
        let i = 0;
        i < intermediateSupportSelects.length;
        i++
    ) {

        currentPosition +=
            spanLengthInputs[i].valueAsNumber;

        positions.push(
            currentPosition
        );
    }


    return positions;
}


function createSupportSymbol(
    type,
    position
) {

    const symbol =
        document.createElement("div");

    symbol.className =
        "support-symbol";

    symbol.style.left =
        `${position}%`;


    if (type === "pinned") {

        symbol.textContent = "△";

    } else if (type === "roller") {

        symbol.textContent = "▽";

    } else if (type === "fixed") {

        symbol.textContent = "▌";
    }


    return symbol;
}


function updateSupports(
    totalLength
) {

    supportsContainer.innerHTML = "";


    const leftType =
        leftSupportSelect.value;

    const rightType =
        rightSupportSelect.value;


    if (leftType !== "free") {

        const leftSymbol =
            createSupportSymbol(
                leftType,
                0
            );

        supportsContainer.appendChild(
            leftSymbol
        );
    }


    if (rightType !== "free") {

        const rightSymbol =
            createSupportSymbol(
                rightType,
                100
            );

        supportsContainer.appendChild(
            rightSymbol
        );
    }


    const supportPositions =
        getIntermediateSupportPositions();


    for (
        let i = 0;
        i < supportPositions.length;
        i++
    ) {

        const type =
            intermediateSupportSelects[i].value;


        const position =
            positionToPercent(
                supportPositions[i],
                totalLength
            );


        const symbol =
            createSupportSymbol(
                type,
                position
            );


        supportsContainer.appendChild(
            symbol
        );
    }
}


function validateHingePositions(
    totalLength
) {

    const positions = [];

    let hasError = false;


    for (
        let i = 0;
        i < hingePositionInputs.length;
        i++
    ) {

        const input =
            hingePositionInputs[i];

        const position =
            Number(input.value);


        input.style.border =
            "1px solid #aaa";


        if (
            !Number.isFinite(position)
            || position <= 0
            || position >= totalLength
        ) {

            input.style.border =
                "2px solid #c62828";

            hasError = true;

            continue;
        }


        const duplicateHinge =
            positions.some(
                existingPosition =>
                    Math.abs(
                        existingPosition
                        - position
                    ) < 1e-9
            );


        if (duplicateHinge) {

            input.style.border =
                "2px solid #c62828";

            hasError = true;

            continue;
        }


        positions.push(position);
    }


    return !hasError;
}


function updateHinges(
    totalLength
) {

    hingesContainer.innerHTML = "";


    const valid =
        validateHingePositions(
            totalLength
        );


    if (!valid) {
        return;
    }


    for (
        let i = 0;
        i < hingePositionInputs.length;
        i++
    ) {

        const position =
            Number(
                hingePositionInputs[i].value
            );


        const percent =
            positionToPercent(
                position,
                totalLength
            );


        const hinge =
            document.createElement("div");

        hinge.className =
            "hinge-symbol";

        hinge.style.left =
            `${percent}%`;


        hingesContainer.appendChild(
            hinge
        );
    }
}


function updateBeam() {

    invalidateSchemeResults();

    const lengths =
        getSpanLengths();

    if (lengths.length === 0) {
        return;
    }


    const totalLength =
        getTotalLength();


    if (totalLength <= 0) {
        return;
    }


    totalLengthElement.textContent =
        `Общая длина: ${totalLength.toFixed(2)} м`;


    separatorsContainer.innerHTML = "";
    dimensionsContainer.innerHTML = "";
    endsContainer.innerHTML = "";


    let currentPosition = 0;


    const leftEnd =
        document.createElement("div");

    leftEnd.className = "end-label";

    leftEnd.style.left = "0%";

    leftEnd.textContent = "A";

    endsContainer.appendChild(
        leftEnd
    );


    for (
        let i = 0;
        i < lengths.length;
        i++
    ) {

        const start =
            currentPosition;

        const end =
            currentPosition + lengths[i];

        const middle =
            start + lengths[i] / 2;


        const dimension =
            document.createElement("div");

        dimension.className = "dimension";

        dimension.style.left =
            `${positionToPercent(
                middle,
                totalLength
            )}%`;

        dimension.textContent =
            `L${i + 1} = ${lengths[i].toFixed(2)} м`;

        dimensionsContainer.appendChild(
            dimension
        );


        if (i < lengths.length - 1) {

            const separator =
                document.createElement("div");

            separator.className =
                "span-separator";

            separator.style.left =
                `${positionToPercent(
                    end,
                    totalLength
                )}%`;

            separatorsContainer.appendChild(
                separator
            );
        }


        currentPosition = end;
    }


    const rightEnd =
        document.createElement("div");

    rightEnd.className = "end-label";

    rightEnd.style.left = "100%";

    rightEnd.textContent = "B";

    endsContainer.appendChild(
        rightEnd
    );


    updateSupports(totalLength);

    updateHinges(totalLength);
}


async function buildScheme() {

    const totalLength =
        getTotalLength();


    const valid =
        validateHingePositions(
            totalLength
        );


    if (!valid) {

        alert(
            "Проверьте координаты внутренних шарниров."
        );

        return;
    }


    const supportData = [];


    const leftType =
        leftSupportSelect.value;

    if (leftType !== "free") {

        supportData.push({
            position: 0,
            support_type: leftType
        });
    }


    const rightType =
        rightSupportSelect.value;

    if (rightType !== "free") {

        supportData.push({
            position: totalLength,
            support_type: rightType
        });
    }


    const intermediatePositions =
        getIntermediateSupportPositions();


    for (
        let i = 0;
        i < intermediateSupportSelects.length;
        i++
    ) {

        supportData.push({
            position:
                intermediatePositions[i],

            support_type:
                intermediateSupportSelects[i].value
        });
    }


    const data = {

        spans: spanLengthInputs.map(
            (input, index) => ({
                length: Number(
                    input.value
                ),

                relative_ei: Number(
                    spanEiInputs[index].value
                )
            })
        ),

        supports: supportData,

        internal_hinges:
            hingePositionInputs.map(
                input => ({
                    position:
                        Number(input.value)
                })
            )
    };


    invalidateSchemeResults();
    const buildRevision = schemeRevision;
    const schemeResult = document.getElementById("scheme-result");

    console.log(
        "Данные для Python:",
        data
    );

    let unstableResponse = false;
    try {

        const response =
            await fetch(
                "/api/build-scheme",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        const result =
            await response.json();

        if (buildRevision !== schemeRevision) return;

        if (!response.ok) {
            unstableResponse = response.headers.get("X-Scheme-Status") === "unstable";
            throw new Error(result.detail || `Ошибка сервера: ${response.status}`);
        }


        console.log(
            "Ответ FastAPI:",
            result
        );


        if (result.status === "ok") {
            setSchemeWarning(false);
            currentSchemeData = data;
            calculateInfluenceButton.disabled = false;
            influenceSection.max = String(result.total_length);
            influenceSection.value = String((result.total_length / 2).toFixed(2));
            influenceSupport.replaceChildren();
            for (const support of data.supports) {
                const option = document.createElement("option");
                option.value = String(support.position);
                option.textContent = `Опора, x = ${Number(support.position).toFixed(2)} м`;
                influenceSupport.appendChild(option);
            }
            schemeResult.textContent =

                `Расчётная схема создана. ` +
                `Пролётов: ${result.number_of_spans}, ` +
                `опор: ${result.number_of_supports}, ` +
                `внутренних шарниров: ${result.number_of_hinges}, ` +
                `степеней свободы: ${result.number_of_dofs}.`;

        } else {
            const detail = result.detail || result.message || "Не удалось построить схему.";
            schemeResult.textContent = `Ошибка: ${detail}`;
            setSchemeWarning(isChangeableSchemeError(detail));
        }


    } catch (error) {

        if (buildRevision !== schemeRevision) return;

        console.error(
            "Ошибка передачи схемы:",
            error
        );

        const isUnstable = unstableResponse || isChangeableSchemeError(error.message);
        schemeResult.textContent = `Ошибка: ${error.message}`;
        setSchemeWarning(isUnstable);
    }
}


spanCountSelect.addEventListener(
    "change",
    createSpanInputs
);


leftSupportSelect.addEventListener(
    "change",
    updateBeam
);


rightSupportSelect.addEventListener(
    "change",
    updateBeam
);


buildSchemeButton.addEventListener(
    "click",
    buildScheme
);

influenceQuantity.addEventListener("change", () => {
    const isReaction = influenceQuantity.value === "R";
    influenceSectionLabel.hidden = isReaction;
    influenceSupportLabel.hidden = !isReaction;
    clearInfluenceResult();
});

influenceSection.addEventListener("input", clearInfluenceResult);
influenceSupport.addEventListener("change", clearInfluenceResult);

calculateInfluenceButton.addEventListener("click", async () => {
    if (!currentSchemeData) return;
    const isReaction = influenceQuantity.value === "R";
    const position = Number(isReaction ? influenceSupport.value : influenceSection.value);
    const numberOfPoints = 101;
    if (!Number.isFinite(position)) {
        influenceResult.textContent = "Укажите корректную координату.";
        return;
    }
    calculateInfluenceButton.disabled = true;
    influenceResult.replaceChildren();
    influenceResult.textContent = "Выполняется расчёт…";
    const requestId = ++influenceRequestId;
    const requestedScheme = currentSchemeData;
    try {
        const response = await fetch("/api/influence", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ...currentSchemeData,
                quantity: influenceQuantity.value,
                position,
                number_of_points: numberOfPoints
            })
        });
        const result = await response.json();
        if (requestId !== influenceRequestId || currentSchemeData !== requestedScheme) return;
        if (!response.ok) throw new Error(result.detail || "Ошибка расчёта линии влияния.");
        renderInfluence(result, getTotalLength(), requestedScheme);
    } catch (error) {
        if (requestId !== influenceRequestId || currentSchemeData !== requestedScheme) return;
        influenceResult.innerHTML = "";
        const message = document.createElement("p");
        message.className = "error-message";
        message.textContent = `Ошибка: ${error.message}`;
        influenceResult.appendChild(message);
    } finally {
        if (requestId === influenceRequestId) {
            calculateInfluenceButton.disabled = !currentSchemeData;
        }
    }
});

function renderInfluence(result, totalLength, scheme) {
    const series = result.quantity === "Q"
        ? [{ values: result.left_values, color: "#1565c0", label: "Слева от сечения" },
           { values: result.right_values, color: "#ef6c00", label: "Справа от сечения" }]
        : [{ values: result.values, color: "#1565c0", label: result.quantity }];
    const allValues = series.flatMap(item => item.values);
    let min = Math.min(0, ...allValues);
    let max = Math.max(0, ...allValues);
    if (max - min < 1e-12) { min -= 1; max += 1; }
    const width = 900, height = 340, left = 64, right = 24, top = 25, bottom = 48;
    const x = value => left + (value / totalLength) * (width - left - right);
    const y = value => top + ((max - value) / (max - min)) * (height - top - bottom);
    const zeroY = y(0);
    const formatValue = value => Number(value).toPrecision(5);
    const valueAt = (values, position) => {
        const positions = result.positions;
        const exactIndex = positions.findIndex(item => Math.abs(item - position) < 1e-9);
        if (exactIndex >= 0) return values[exactIndex];
        let rightIndex = positions.findIndex(item => item > position);
        if (rightIndex <= 0) return values[Math.max(0, rightIndex)];
        const leftIndex = rightIndex - 1;
        const ratio = (position - positions[leftIndex]) / (positions[rightIndex] - positions[leftIndex]);
        return values[leftIndex] + ratio * (values[rightIndex] - values[leftIndex]);
    };
    const ordinateLabels = (position, support = false) => {
        const labelX = x(position);
        return series.map((item, index) => {
            const value = valueAt(item.values, position);
            const labelY = y(value);
            const label = formatValue(value);
            const offset = index === 0 ? -7 : 13;
            return `<text x="${labelX.toFixed(2)}" y="${(labelY + offset).toFixed(2)}" text-anchor="middle" font-size="11" fill="${item.color}" stroke="white" stroke-width="3" paint-order="stroke">${label}</text>`;
        }).join("");
    };
    const supportSymbols = scheme.supports.map(support => {
        const markerX = x(Number(support.position));
        const beamY = zeroY;
        const type = support.support_type;
        let symbol;
        if (type === "pinned") {
            symbol = `<polygon points="${markerX},${beamY - 7} ${markerX - 8},${beamY + 6} ${markerX + 8},${beamY + 6}" fill="#111"/>`;
        } else if (type === "roller") {
            symbol = `<polygon points="${markerX},${beamY + 7} ${markerX - 8},${beamY - 6} ${markerX + 8},${beamY - 6}" fill="#111"/>`;
        } else if (type === "fixed") {
            symbol = `<line x1="${markerX}" y1="${beamY - 11}" x2="${markerX}" y2="${beamY + 11}" stroke="#111" stroke-width="4"/>`;
        } else {
            symbol = `<polygon points="${markerX},${beamY + 7} ${markerX - 8},${beamY - 6} ${markerX + 8},${beamY - 6}" fill="#111"/>`;
        }
        return `${symbol}${ordinateLabels(Number(support.position), true)}`;
    }).join("");
    const hingeSymbols = scheme.internal_hinges.map(hinge => {
        const markerX = x(Number(hinge.position));
        const beamY = zeroY;
        return `<circle cx="${markerX}" cy="${beamY}" r="5" fill="white" stroke="#2e7d32" stroke-width="2"/>${ordinateLabels(Number(hinge.position))}`;
    }).join("");
    const sectionTick = result.quantity === "R" ? "" :
        `<line x1="${x(result.target_position).toFixed(2)}" y1="${top}" x2="${x(result.target_position).toFixed(2)}" y2="${height - bottom}" stroke="#d32f2f" stroke-width="1"/>`;
    const areas = series.map(item => {
        const points = item.values.map((value, index) => `${x(result.positions[index]).toFixed(2)},${y(value).toFixed(2)}`);
        const areaPath = `M${x(result.positions[0]).toFixed(2)},${zeroY.toFixed(2)} L${points.join(" L")} L${x(result.positions[result.positions.length - 1]).toFixed(2)},${zeroY.toFixed(2)} Z`;
        return `<path d="${areaPath}" fill="#90caf9" fill-opacity="0.55" stroke="none"/>`;
    }).join("");
    const paths = series.map(item => {
        const points = item.values.map((value, index) => `${x(result.positions[index]).toFixed(2)},${y(value).toFixed(2)}`);
        return `<path d="M${points.join(" L")}" fill="none" stroke="${item.color}" stroke-width="2.5"/>`;
    }).join("");
    const endClosures = series.map(item => {
        const firstX = x(result.positions[0]).toFixed(2);
        const lastX = x(result.positions[result.positions.length - 1]).toFixed(2);
        return `<line x1="${firstX}" y1="${zeroY.toFixed(2)}" x2="${firstX}" y2="${y(item.values[0]).toFixed(2)}" stroke="${item.color}" stroke-width="2"/><line x1="${lastX}" y1="${zeroY.toFixed(2)}" x2="${lastX}" y2="${y(item.values[item.values.length - 1]).toFixed(2)}" stroke="${item.color}" stroke-width="2"/>`;
    }).join("");
    const title = result.quantity === "R" ? `R, опора x = ${result.target_position.toFixed(2)} м`
        : `${result.quantity}, сечение x = ${result.target_position.toFixed(2)} м`;
    const legend = series.map(item => `<span style="color:${item.color};margin-right:18px">● ${item.label}</span>`).join("");
    const statistics = series.map(item => {
        const seriesMin = Math.min(...item.values);
        const seriesMax = Math.max(...item.values);
        return `<div>${item.label}: минимум ${formatValue(seriesMin)}, максимум ${formatValue(seriesMax)}</div>`;
    }).join("");
    influenceResult.innerHTML = `<strong>${title}</strong><div>${legend}</div>
        <div class="influence-stats">${statistics}</div>
        <svg id="influence-chart" viewBox="0 0 ${width} ${height}" role="img" aria-label="График линии влияния ${result.quantity}">
        ${areas}
        <line x1="${left}" y1="${zeroY}" x2="${width-right}" y2="${zeroY}" stroke="#777" stroke-width="2.5"/>
        ${paths}
        ${endClosures}
        ${supportSymbols}
        ${hingeSymbols}
        ${sectionTick}
        <text x="${left-8}" y="${top+5}" text-anchor="end">${max.toPrecision(4)}</text>
        <text x="${left-8}" y="${height-bottom}" text-anchor="end">${min.toPrecision(4)}</text>
        </svg>`;
}


async function refreshSiteStats() {
    try {
        const response = await fetch("/api/stats", { cache: "no-store" });
        if (!response.ok) return;
        const stats = await response.json();
        document.getElementById("visitor-count").textContent =
            Number(stats.visitors).toLocaleString("ru-RU");
    } catch (error) {
        // Статистика не должна мешать работе калькулятора.
    }
}


createSpanInputs();
refreshSiteStats();
