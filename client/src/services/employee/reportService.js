async function handleApiResponse(res) {
    const contentType = res.headers.get('content-type');
    let data;

    if (contentType && contentType.includes('application/json')) {
        data = await res.json();
    } else {
        const text = await res.text();
        console.error('Resposta não JSON recebida:', text);
        throw new Error('Resposta do servidor não está em formato JSON esperado.');
    }

    if (!res.ok) {
        const errorMsg = data?.erro || res.statusText || 'Erro desconhecido ao processar requisição.';
        console.error('Erro de resposta da API:', res.status, errorMsg);
        throw new Error(errorMsg);
    }
    return data;
}

export async function getTiposRelatorio() {
    try {
        const res = await fetch('http://localhost:5000/api/funcionario/relatorios/tipos', {
            method: 'GET',
            credentials: 'include',
        });
        return await handleApiResponse(res);
    } catch (error) {
        console.error('Erro ao listar tipos de relatório:', error);
        throw error;
    }
}

export async function gerarRelatorioJSON(reportOptions) {
    try {
        const payload = {
            tipo_relatorio: reportOptions.tipo_relatorio,
            start_date: reportOptions.start_date,
            end_date: reportOptions.end_date,
            limit: reportOptions.limit,
            ...(reportOptions.customFilters || {}) 
        };

        const res = await fetch('http://localhost:5000/api/funcionario/relatorios/gerar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(payload),
        });
        return await handleApiResponse(res);
    } catch (error) {
        console.error('Erro ao gerar relatório JSON:', error);
        throw error;
    }
}

export async function gerarRelatorioPDF(reportOptions) {
    try {
        const payload = {
            tipo_relatorio: reportOptions.tipo_relatorio,
            start_date: reportOptions.start_date,
            end_date: reportOptions.end_date,
            limit: reportOptions.limit,
            ...(reportOptions.customFilters || {})
        };

        const res = await fetch('http://localhost:5000/api/funcionario/relatorios/pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(payload),
        });

        if (!res.ok) {
            const contentType = res.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const errorData = await res.json();
                const errorMsg = errorData?.erro || res.statusText || 'Erro desconhecido ao gerar PDF.';
                console.error('Erro da API ao gerar PDF (JSON):', res.status, errorMsg);
                throw new Error(errorMsg);
            } else {
                const text = await res.text();
                console.error('Erro da API ao gerar PDF (Texto):', res.status, text);
                throw new Error('Erro ao gerar PDF. Resposta inesperada do servidor.');
            }
        }

        const blob = await res.blob();
        return blob;

    } catch (error) {
        console.error('Erro ao gerar relatório PDF:', error);
        throw error;
    }
}
