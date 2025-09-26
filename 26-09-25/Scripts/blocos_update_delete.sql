-- Bloco 1: UPDATE com Estrutura de Decisão
-- Objetivo: Atualizar o status de um recurso específico, garantindo que ele exista antes.
-- Operação: UPDATE na tabela TB_MEDI_RECURSO.
-- Variáveis: ID do recurso e o novo status.
DECLARE
    -- Variáveis de entrada para a operação
    v_id_recurso_alvo   TB_MEDI_RECURSO.id_recurso%TYPE := 1; -- Altere aqui para testar com outro ID
    v_novo_status       TB_MEDI_RECURSO.st_recurso%TYPE := 'Manutenção';
    
    -- Variável de controle para verificar a existência do registro
    v_contador          NUMBER;

BEGIN
    -- Passo 1: Verifica se o recurso com o ID especificado existe
    SELECT COUNT(*)
    INTO v_contador
    FROM TB_MEDI_RECURSO
    WHERE id_recurso = v_id_recurso_alvo;

    -- Passo 2: Estrutura de decisão (IF)
    IF v_contador > 0 THEN
        -- Se o recurso existe, executa o UPDATE
        UPDATE TB_MEDI_RECURSO
        SET st_recurso = v_novo_status
        WHERE id_recurso = v_id_recurso_alvo;
        
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('SUCESSO: O status do recurso com ID ' || v_id_recurso_alvo || ' foi atualizado para "' || v_novo_status || '".');
    ELSE
        -- Se o recurso não existe, informa o usuário
        DBMS_OUTPUT.PUT_LINE('FALHA: Recurso com ID ' || v_id_recurso_alvo || ' não encontrado. Nenhuma alteração foi feita.');
    END IF;

EXCEPTION
    -- Tratamento de erros inesperados
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('ERRO: Ocorreu um erro inesperado. A transação foi revertida.');
        DBMS_OUTPUT.PUT_LINE('Detalhes do erro: ' || SQLERRM);
END;
/

-- Bloco 2: DELETE (Soft Delete) com Estrutura de Decisão
-- Objetivo: Marcar um usuário como deletado (soft delete), verificando se ele existe e não está deletado.
-- Operação: UPDATE (para o soft delete) na tabela TB_MEDI_USUARIO.
-- Variáveis: Email do usuário a ser deletado.
DECLARE
    -- Variável de entrada
    v_email_alvo        TB_MEDI_USUARIO.ds_email%TYPE := 'carlos.santana@email.com'; -- Altere para testar
    
    -- Variáveis de controle
    v_id_usuario        TB_MEDI_USUARIO.id_usuario%TYPE;
    v_deleted_status    TB_MEDI_USUARIO.deleted%TYPE;

BEGIN
    -- Passo 1: Tenta encontrar o usuário pelo email e obter seu ID e status de deleção
    BEGIN
        SELECT id_usuario, deleted
        INTO v_id_usuario, v_deleted_status
        FROM TB_MEDI_USUARIO
        WHERE ds_email = v_email_alvo;
    EXCEPTION
        -- Se nenhum usuário for encontrado, o SELECT lança NO_DATA_FOUND
        WHEN NO_DATA_FOUND THEN
            v_id_usuario := NULL;
    END;

    -- Passo 2: Estrutura de decisão (IF-ELSIF-ELSE)
    IF v_id_usuario IS NOT NULL THEN
        -- Se o usuário foi encontrado...
        IF v_deleted_status = 0 THEN
            -- ...e não está deletado, executa o soft delete.
            UPDATE TB_MEDI_USUARIO
            SET deleted = 1
            WHERE id_usuario = v_id_usuario;
            
            COMMIT;
            DBMS_OUTPUT.PUT_LINE('SUCESSO: O usuário com email ' || v_email_alvo || ' foi marcado como deletado.');
        ELSE
            -- ...mas já está deletado, informa o usuário.
            DBMS_OUTPUT.PUT_LINE('INFO: O usuário com email ' || v_email_alvo || ' já estava deletado.');
        END IF;
    ELSE
        -- Se o usuário não foi encontrado, informa o usuário.
        DBMS_OUTPUT.PUT_LINE('FALHA: Usuário com email ' || v_email_alvo || ' não encontrado.');
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('ERRO: Ocorreu um erro inesperado. A transação foi revertida.');
        DBMS_OUTPUT.PUT_LINE('Detalhes do erro: ' || SQLERRM);
END;
/
