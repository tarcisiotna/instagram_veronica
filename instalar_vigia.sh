#!/usr/bin/env bash
# Instala o vigia de aprovação como timer do systemd (usuário).
#
#   ./instalar_vigia.sh            # instala e liga (a cada 5 min)
#   ./instalar_vigia.sh --remover  # desliga e remove
#
# O timer roda enquanto a sessão do usuário existe. Para continuar rodando
# depois do logout (ou antes do primeiro login), habilite o linger:
#   loginctl enable-linger "$USER"

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICO="$UNIT_DIR/vigia-aprovacao.service"
TIMER="$UNIT_DIR/vigia-aprovacao.timer"

if [[ "${1:-}" == "--remover" ]]; then
  systemctl --user disable --now vigia-aprovacao.timer 2>/dev/null || true
  rm -f "$SERVICO" "$TIMER"
  systemctl --user daemon-reload
  echo "✅ vigia removido"
  exit 0
fi

mkdir -p "$UNIT_DIR"
sed "s|@DIR@|$DIR|g" "$DIR/systemd/vigia-aprovacao.service" > "$SERVICO"
cp "$DIR/systemd/vigia-aprovacao.timer" "$TIMER"

systemctl --user daemon-reload
systemctl --user enable --now vigia-aprovacao.timer

echo "✅ vigia instalado"
systemctl --user list-timers vigia-aprovacao.timer --no-pager

if [[ "$(loginctl show-user "$USER" -p Linger --value 2>/dev/null || echo no)" != "yes" ]]; then
  echo
  echo "ℹ️  O timer só roda com a sessão aberta. Para rodar sempre:"
  echo "    loginctl enable-linger $USER"
fi
