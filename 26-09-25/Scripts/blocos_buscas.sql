-- Bloco 1: INNER JOIN
-- Objetivo: Listar o total de agendamentos por tipo em cada unidade de saúde.
-- Junção: TB_MEDI_AGENDAMENTO com TB_MEDI_UNIDADE_SAUDE.
-- Agrupamento: Por nome da unidade e tipo de agendamento.
-- Ordenação: Por nome da unidade.
DECLARE
    -- Declaração de variáveis para armazenar os dados do cursor
    v_nm_unidade TB_MEDI_UNIDADE_SAUDE.nm_unidade%TYPE;
    v_tp_agendamento TB_MEDI_AGENDAMENTO.tp_agendamento%TYPE;
    v_total_agendamentos NUMBER;
    
    -- Declaração do cursor que executa a consulta com INNER JOIN
    CURSOR c_agendamentos_por_unidade IS
        SELECT
            u.nm_unidade,
            a.tp_agendamento,
            COUNT(a.id_agendamento) AS total_agendamentos
        FROM
            TB_MEDI_UNIDADE_SAUDE u
        INNER JOIN
            TB_MEDI_AGENDAMENTO a ON u.id_unidade_saude = a.id_unidade_saude
        GROUP BY
            u.nm_unidade,
            a.tp_agendamento
        ORDER BY
            u.nm_unidade;

BEGIN
    DBMS_OUTPUT.PUT_LINE('--- RELATÓRIO: TOTAL DE AGENDAMENTOS POR UNIDADE (INNER JOIN) ---');
    DBMS_OUTPUT.PUT_LINE('UNIDADE | TIPO DE AGENDAMENTO | TOTAL');
    DBMS_OUTPUT.PUT_LINE('-----------------------------------------------------------------');
    
    -- Abre o cursor
    OPEN c_agendamentos_por_unidade;
    
    -- Loop para percorrer os resultados do cursor
    LOOP
        FETCH c_agendamentos_por_unidade INTO v_nm_unidade, v_tp_agendamento, v_total_agendamentos;
        EXIT WHEN c_agendamentos_por_unidade%NOTFOUND;
        
        -- Exibe os resultados formatados
        DBMS_OUTPUT.PUT_LINE(v_nm_unidade || ' | ' || v_tp_agendamento || ' | ' || v_total_agendamentos);
    END LOOP;
    
    -- Fecha o cursor
    CLOSE c_agendamentos_por_unidade;
    DBMS_OUTPUT.PUT_LINE('--- FIM DO RELATÓRIO ---');
END;
/

-- Bloco 2: LEFT JOIN
-- Objetivo: Listar todos os colaboradores e a quantidade de agendamentos associados a cada um.
--           Colaboradores sem agendamentos também serão listados com contagem 0.
-- Junção: TB_MEDI_USUARIO com TB_MEDI_COLABORADOR e TB_MEDI_AGENDAMENTO.
-- Agrupamento: Por nome do colaborador.
-- Ordenação: Pela quantidade de agendamentos, em ordem decrescente.
DECLARE
    v_nm_colaborador TB_MEDI_USUARIO.nm_usuario%TYPE;
    v_total_agendamentos NUMBER;

    CURSOR c_agendamentos_por_colaborador IS
        SELECT
            u.nm_usuario,
            COUNT(a.id_agendamento) AS total_agendamentos
        FROM
            TB_MEDI_COLABORADOR c
        JOIN
            TB_MEDI_USUARIO u ON c.id_usuario = u.id_usuario
        LEFT JOIN
            TB_MEDI_AGENDAMENTO a ON c.id_colaborador = a.id_colaborador
        GROUP BY
            u.nm_usuario
        ORDER BY
            total_agendamentos DESC;

BEGIN
    DBMS_OUTPUT.PUT_LINE(CHR(10)); -- Adiciona uma linha em branco para separar os relatórios
    DBMS_OUTPUT.PUT_LINE('--- RELATÓRIO: AGENDAMENTOS POR COLABORADOR (LEFT JOIN) ---');
    DBMS_OUTPUT.PUT_LINE('COLABORADOR | TOTAL DE AGENDAMENTOS');
    DBMS_OUTPUT.PUT_LINE('---------------------------------------------------------');
    
    OPEN c_agendamentos_por_colaborador;
    
    LOOP
        FETCH c_agendamentos_por_colaborador INTO v_nm_colaborador, v_total_agendamentos;
        EXIT WHEN c_agendamentos_por_colaborador%NOTFOUND;
        
        DBMS_OUTPUT.PUT_LINE(v_nm_colaborador || ' | ' || v_total_agendamentos);
    END LOOP;
    
    CLOSE c_agendamentos_por_colaborador;
    DBMS_OUTPUT.PUT_LINE('--- FIM DO RELATÓRIO ---');
END;
/

-- Bloco 3: RIGHT JOIN
-- Objetivo: Listar todos os tipos de recursos e contar quantos agendamentos foram feitos para cada tipo.
--           Recursos que nunca foram agendados também aparecerão na lista com contagem 0.
-- Junção: TB_MEDI_AGENDAMENTO com TB_MEDI_RECURSO.
-- Agrupamento: Por tipo de recurso.
-- Ordenação: Por tipo de recurso.
DECLARE
    v_tp_recurso TB_MEDI_RECURSO.tp_recurso%TYPE;
    v_total_utilizacoes NUMBER;

    CURSOR c_utilizacao_por_recurso IS
        SELECT
            r.tp_recurso,
            COUNT(a.id_agendamento) AS total_utilizacoes
        FROM
            TB_MEDI_AGENDAMENTO a
        RIGHT JOIN
            TB_MEDI_RECURSO r ON a.id_recurso = r.id_recurso
        GROUP BY
            r.tp_recurso
        ORDER BY
            r.tp_recurso;

BEGIN
    DBMS_OUTPUT.PUT_LINE(CHR(10));
    DBMS_OUTPUT.PUT_LINE('--- RELATÓRIO: UTILIZAÇÃO POR TIPO DE RECURSO (RIGHT JOIN) ---');
    DBMS_OUTPUT.PUT_LINE('TIPO DE RECURSO | VEZES UTILIZADO');
    DBMS_OUTPUT.PUT_LINE('--------------------------------------------------------------');
    
    OPEN c_utilizacao_por_recurso;
    
    LOOP
        FETCH c_utilizacao_por_recurso INTO v_tp_recurso, v_total_utilizacoes;
        EXIT WHEN c_utilizacao_por_recurso%NOTFOUND;
        
        DBMS_OUTPUT.PUT_LINE(v_tp_recurso || ' | ' || v_total_utilizacoes);
    END LOOP;
    
    CLOSE c_utilizacao_por_recurso;
    DBMS_OUTPUT.PUT_LINE('--- FIM DO RELATÓRIO ---');
END;
/
