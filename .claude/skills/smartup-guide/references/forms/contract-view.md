# Contract View

Tags: contract, contract-view, view-form, locator, screenshot, order-precondition

## Quick Lookup

- Form slug: `contract-view`
- Navigation: `Финансы > Договоры` -> contract row -> `Просмотр`
- URL pattern: `*/anor/mkf/contract_view`
- Page container: `b-page`
- Main test file: `tests/smoke/test_groups/test_A_grup/test_contract.py`
- Main flow files:
  - `tests/smoke/flows/flow_contract/flow_contract_list.py`
  - `tests/smoke/flows/flow_contract/flow_contract_add.py`
- Related domain docs:
  - `../contracts.md`
  - `../ui-patterns.md`
  - `../testing-debug.md`

## Screenshot Paths

- Screenshot archive folder: `references/forms/screenshots/contract-view/`
- Metadata folder: `references/forms/screenshots/contract-view/`
- Expected file naming:
  - `contract-view__default__desktop-1440x783__<contract_code>.png`
  - metadata: `contract-view__default__desktop-1440x783__<contract_code>.json`
- If screenshot is missing, open contract view in stable UI state, take screenshot, save it to `references/forms/screenshots/contract-view/`, save metadata in the same folder, and update this section with exact file path.
- Visual regression note: loader, dropdown, confirm/error modal, and transient notifications must be closed/hidden before taking baseline-ready screenshot.

## Open Flow

1. Open contract list: `flow_open_contract_list(page)`.
2. Search/select by contract code: `flow_contract_list(page, find_code=contract_code)`.
3. Open view: `flow_contract_list(page, view=True)`.
4. Assert URL: `expect(page).to_have_url(re.compile(r".*/anor/mkf/contract_view"))`.

## Known Locators

- Page root: `page.locator("b-page")`
- Contract row in list: `page.locator("b-grid").get_by_text(contract_code).first`
- View button: `page.get_by_role("button", name="Просмотр", exact=True)`
- Close button: `page.get_by_role("button", name="Закрыть", exact=True)`

## Current View Assertions

For A-group order contract:

- `contract_code`
- `contract_name`
- `natural_client-pw{code}`
- `Узбекский сум`
- `500000`

For payment type contract:

- same as above
- `Перечисление` if contract was created with `Типы оплат = Перечисление`

## Related Business Rules

- Contract code and name are saved to `data_store.json` for order tests.
- Order form selects contract by `contract_name`, not by contract code.
- Contract `Сумма договора` is used as order total amount limit.
- Contract `Типы оплат` auto-fills order `Тип оплаты`, but user may change it; validation is still based on sum limit.
- Contract currency filters products in order; changing to another currency contract clears already selected products.

## Known Debug Notes

- Contract list grid may not display every contract field. If a field is needed for list search/assert, enable its column/search through grid setting.
- View assertions should use visible page text in `b-page`; input-like values may need label/input helper if they are not included in text.
- During debug iteration, if `contract_code` / `contract_name` already exist in `data_store.json`, reuse them instead of recreating contract.
